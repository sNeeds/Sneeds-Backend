from rest_framework import serializers

from sNeeds.apps.account.serializers import StudentDetailedInfoBaseSerializer, UniversitySerializer, CountrySerializer, \
    StudentFormApplySemesterYearSerializer
from sNeeds.apps.similarApply.models import AppliedStudentDetailedInfo, AppliedTo


class AppliedToSerializer(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    major = serializers.SerializerMethodField()
    semester_year = StudentFormApplySemesterYearSerializer()

    class Meta:
        model = AppliedTo
        fields = [
            'id', 'student_detailed_info',
            'country', 'university', 'grade', 'major', 'semester_year', 'fund',
            'accepted', 'comment'
        ]

    def get_semester_year(self, obj):
        return obj.semester_year.name

    def get_major(self, obj):
        return obj.major.name

    def get_grade(self, obj):
        return obj.grade.name

    def get_university(self, obj):
        university = obj.university
        return UniversitySerializer(
            university, context={"request": self.context.get("request")}
        ).data

    def get_country(self, obj):
        country = obj.country
        return CountrySerializer(
            country, context={"request": self.context.get("request")}
        ).data


class AppliedStudentDetailedInfoSerializer(StudentDetailedInfoBaseSerializer):
    applied_to = serializers.SerializerMethodField()

    class Meta(StudentDetailedInfoBaseSerializer.Meta):
        model = AppliedStudentDetailedInfo
        fields = StudentDetailedInfoBaseSerializer.Meta.fields + [
            'applied_to',
        ]

    def get_applied_to(self, obj):
        try:
            applied_to_obj = AppliedTo.objects.get(student_detailed_info__id=obj.id)
            data = AppliedToSerializer(applied_to_obj).data
        except AppliedTo.DoesNotExist:
            data = None

        return data
