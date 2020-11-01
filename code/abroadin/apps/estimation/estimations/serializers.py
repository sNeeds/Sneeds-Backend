from rest_framework import serializers

from abroadin.apps.estimation.form.models import WantToApply
from abroadin.apps.estimation.estimations.classes import ValueRange
from abroadin.apps.estimation.estimations.values import VALUES_WITH_ATTRS
from apps.estimation.estimations.chances import AdmissionChance


class WantToApplyChanceSerializer(serializers.Serializer):
    universities = serializers.SerializerMethodField()

    class Meta:
        model = WantToApply
        fields = [
            'id',
            'universities',
        ]

    def get_universities(self, obj):
        data = []
        admission_chance = AdmissionChance(obj.student_detailed_info)

        for university in obj.universities.all().order_by('rank'):
            data.append(admission_chance.get_university_chance_with_label(university))

        return data
