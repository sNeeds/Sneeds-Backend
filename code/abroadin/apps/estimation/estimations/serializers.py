from rest_framework import serializers

from abroadin.apps.estimation.form.models import WantToApply
from abroadin.apps.estimation.estimations.classes import ValueRange
from abroadin.apps.estimation.estimations.values import VALUES_WITH_ATTRS


class WantToApplyChanceSerializer(serializers.Serializer):
    universities = serializers.SerializerMethodField()

    class Meta:
        model = WantToApply
        fields = [
            'id',
            'universities',
        ]

    def get_universities(self, obj):
        universities_with_chance_list = []
        value_range = ValueRange(VALUES_WITH_ATTRS["admission_chance_value_to_label"])

        for university in obj.universities.all().order_by('rank'):
            rank = university.rank

            universities_with_chance_list.append({
                "university": university.name,
                "rank": university.rank,
                "chances": {
                    "admission": value_range.find_value_attrs(value, label),
                    "admission_value": None,
                    "scholarship": None,
                    "scholarship_value": None,
                    "full_fund": None,
                    "full_fund_value": None
                }
            }
            )


            elif 401 <= uni.rank:
            append_dict["chances"] = {
                "admission": "High",
                "admission_value": 1,
                "scholarship": "High",
                "scholarship_value": 1,
                "full_fund": "High",
                "full_fund_value": 1
            }

        (append_dict)

    return universities_with_chance_list
