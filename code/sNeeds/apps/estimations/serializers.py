from rest_framework import serializers

from sNeeds.apps.account.models import WantToApply


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
        for uni in obj.universities.all().order_by('rank'):
            append_dict = {
                "university": uni.name,
                "rank": uni.rank,
                "chances": {
                    "admission": None,
                    "admission_value": None,
                    "scholarship": None,
                    "scholarship_value": None,
                    "full_fund": None,
                    "full_fund_value": None
                }
            }

            if uni.rank < 20:
                append_dict["chances"] = {
                    "admission": "Medium",
                    "admission_value": 0.4,
                    "scholarship": "Very low",
                    "scholarship_value": 0,
                    "full_fund": "Very low",
                    "full_fund_value": 0
                }
            elif 20 <= uni.rank < 100:
                append_dict["chances"] = {
                    "admission": "High",
                    "admission_value": 0.8,
                    "scholarship": "Medium",
                    "scholarship_value": 0.5,
                    "full-fund": "Low",
                    "full_fund_value": 0.3
                }

            elif 100 <= uni.rank < 400:
                append_dict["chances"] = {
                    "admission": "Very High",
                    "admission_value": 1,
                    "scholarship": "High",
                    "scholarship_value": 0.95,
                    "full_fund": "Medium",
                    "full_fund_value": 0.9
                }
            else:
                append_dict["chances"] = {
                    "admission": "High",
                    "admission_value": 1,
                    "scholarship": "High",
                    "scholarship_value": 1,
                    "full_fund": "High",
                    "full_fund_value": 1
                }

            universities_with_chance_list.append(append_dict)

        return universities_with_chance_list
