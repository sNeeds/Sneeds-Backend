from abroadin.apps.estimation.estimations.classes import ValueRange
from abroadin.apps.data.applydata.values.values import VALUES_WITH_ATTRS


class AdmissionChance:
    def __init__(self, student_detailed_info):
        self.form = student_detailed_info

    def _get_label_chance(self, value, value_with_attr_key, label, *args, **kwargs):
        values_with_attrs = kwargs.get('values_with_attrs', VALUES_WITH_ATTRS)
        value_range = ValueRange(values_with_attrs['admission_chance'][value_with_attr_key])
        return value_range.find_value_attrs(value, label)

    def _get_all_chances(self, value, value_with_attr_key, *args, **kwargs):
        data = {
            "admission": self._get_label_chance(value, value_with_attr_key, "admission", *args, **kwargs),
            "scholarship": self._get_label_chance(value, value_with_attr_key, "scholarship", *args, **kwargs),
            "full_fund": self._get_label_chance(value, value_with_attr_key, "full_fund", *args, **kwargs)
        }
        return data

    def get_1_to_20_chance(self, *args, **kwargs):
        return self._get_all_chances(
            self.form.value,
            "1_20_university_rank_admission_chance",
            *args, **kwargs
        )

    def get_21_to_100_chance(self, *args, **kwargs):
        return self._get_all_chances(
            self.form.value,
            "21_100_university_rank_admission_chance",
            *args, **kwargs
        )

    def get_101_to_400_chance(self, *args, **kwargs):
        return self._get_all_chances(
            self.form.value,
            "101_400_university_rank_admission_chance",
            *args, **kwargs
        )

    def get_401_above_chance(self, *args, **kwargs):
        return self._get_all_chances(
            self.form.value,
            "401_above_university_rank_admission_chance",
            *args, **kwargs
        )

    def get_university_chance(self, university):
        rank = university.rank

        if rank < 21:
            return self.get_1_to_20_chance()
        elif 21 <= rank < 101:
            return self.get_21_to_100_chance()
        elif 101 <= rank < 401:
            return self.get_101_to_400_chance()
        elif 401 <= rank:
            return self.get_401_above_chance()

    def get_university_chance_with_label(self, university, *args, **kwargs):
        values_with_attrs = kwargs.get('values_with_attrs', VALUES_WITH_ATTRS)

        data = self.get_university_chance(university)

        value_range = ValueRange(values_with_attrs['admission_chance']['label'])
        for key, value in data.copy().items():
            data[key + "_label"] = value_range.find_value_attrs(value, 'label')

        return data

    def convert_value_to_label(self, value, *args, **kwargs):
        values_with_attrs = kwargs.get('values_with_attrs', VALUES_WITH_ATTRS)

        value_range = ValueRange(values_with_attrs['admission_chance']['label'])
        return value_range.find_value_attrs(value, 'label')