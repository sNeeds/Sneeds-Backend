from rest_framework import serializers

from sNeeds.apps.similarApply.models import AppliedStudentDetailedInfo


class AppliedStudentDetailedInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedStudentDetailedInfo
        fields = ['id', 'universities', 'discount', 'url', 'code', ]
