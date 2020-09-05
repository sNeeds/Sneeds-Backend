from rest_framework import serializers

from sNeeds.apps.account.serializers import StudentDetailedInfoBaseSerializer
from sNeeds.apps.similarApply.models import AppliedStudentDetailedInfo, AppliedTo


class AppliedToSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id', 'student_detailed_info',
            'country', 'university', 'grade', 'major', 'semester_year', 'fund',
            'accepted', 'comment'
        ]


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
            data = AppliedToSerializer(applied_to_obj)
        except AppliedTo.DoesNotExist:
            data = None

        return data
