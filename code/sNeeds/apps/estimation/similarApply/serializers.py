from rest_framework import serializers

from sNeeds.apps.users.account.serializers import StudentDetailedInfoBaseSerializer, UniversitySerializer
from sNeeds.apps.estimation.similarApply.models import AppliedStudentDetailedInfo, AppliedTo


class AppliedToSerializer(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    class Meta:
        model = AppliedTo
        fields = [
            'university', 'grade', 'fund',
            'accepted', 'comment'
        ]

    def get_grade(self, obj):
        return obj.grade.name

    def get_university(self, obj):
        university = obj.university
        return UniversitySerializer(
            university, context={"request": self.context.get("request")}
        ).data


class AppliedStudentDetailedInfoSerializer(StudentDetailedInfoBaseSerializer):
    home_university = serializers.SerializerMethodField()
    home_university_gpa = serializers.SerializerMethodField()
    applied_to = serializers.SerializerMethodField()

    class Meta(StudentDetailedInfoBaseSerializer.Meta):
        model = AppliedStudentDetailedInfo
        fields = [
            'home_university',
            'home_university_gpa',
            'applied_to'
        ]

    def get_home_university(self, obj):
        last_university_through = obj.get_last_university_through()
        return last_university_through.university.name if last_university_through is not None else None

    def get_home_university_gpa(self, obj):
        last_university_through = obj.get_last_university_through()
        return last_university_through.gpa if last_university_through is not None else None

    def get_applied_to(self, obj):
        try:
            applied_to_obj = AppliedTo.objects.filter(applied_student_detailed_info__id=obj.id)
            data = AppliedToSerializer(applied_to_obj, many=True).data
        except AppliedTo.DoesNotExist:
            data = None

        return data
