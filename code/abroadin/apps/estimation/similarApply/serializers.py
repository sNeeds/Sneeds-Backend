from rest_framework import serializers

from abroadin.apps.data.account.serializers import UniversitySerializer
from abroadin.apps.estimation.similarApply.models import AppliedTo


class AppliedToSerializer(serializers.ModelSerializer):
    applied_university = serializers.SerializerMethodField()

    class Meta:
        model = AppliedTo
        fields = [
            'applied_university', 'grade', 'fund', 'accepted', 'comment'
        ]

    def get_applied_university(self, obj):
        university = obj.university
        return UniversitySerializer(
            university, context={"request": self.context.get("request")}
        ).data


class AppliedToExtendedSerializer(AppliedToSerializer):
    home_university = serializers.SerializerMethodField()
    home_university_gpa = serializers.SerializerMethodField()
    language_certificate = serializers.SerializerMethodField()

    class Meta(AppliedToSerializer.Meta):
        fields = AppliedToSerializer.Meta.fields + [
            'home_university', 'home_university_gpa', 'language_certificate'
        ]

    def get_language_certificate(self, obj):
        return obj.applied_student_detailed_info.language_certificates_str()

    def get_home_university(self, obj):
        form = obj.applied_student_detailed_info
        last_university_through = form.last_university_through()
        return last_university_through.university.name if last_university_through is not None else None

    def get_home_university_gpa(self, obj):
        form = obj.applied_student_detailed_info
        last_university_through = form.last_university_through()
        return last_university_through.gpa if last_university_through is not None else None
