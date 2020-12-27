from django.db import models
from django.db.models import When, Q, Value, IntegerField, Case

from abroadin.apps.data.applydata.classes import ValueRange
from abroadin.apps.data.applydata.values import VALUES_WITH_ATTRS
from abroadin.base.mixins.manager import GetListManagerMixin


class GradeQuerySetManager(GetListManagerMixin, models.QuerySet):
    pass


class EducationQuerySetManager(models.QuerySet):
    def order_by_grade(self):
        """
            Returns from lower to higher grade. e.g, Bachelor, Master, ...
        """
        from .models import GradeChoices

        q_list = []
        when_list = []

        for grade in GradeChoices.get_ordered():
            q = Q(grade=grade)
            when = When(q, then=Value(GradeChoices.order_num(grade)))

            q_list.append(q)
            when_list.append(when)

        qs = self.all().annotate(
            grade_ordering=Case(*when_list, output_field=IntegerField())
        ).order_by('grade_ordering')

        return qs


class PublicationQuerySetManager(models.QuerySet):

    @classmethod
    def calculate_value(cls, qs):
        total_val = 0.0
        counter = 0.0
        for publication in qs:
            total_val += max((publication.value - counter), 0)
            counter += 0.3
        total_val = min(total_val, 1)
        return total_val

    def total_value(self):
        qs = self.all().order_by('-value')
        return self.calculate_value(qs)

    def total_value_label(self):
        value_range = ValueRange(VALUES_WITH_ATTRS["publication_qs"])
        label = value_range.find_value_attrs(self.total_value(), 'label')

        return label


class LanguageCertificateQuerySetManager(models.QuerySet):
    def get_from_type_or_none(self, certificate_type):
        from abroadin.apps.estimation.form.models import LanguageCertificate
        try:
            return self.get(certificate_type=certificate_type)
        except LanguageCertificate.DoesNotExist:
            return None

    def get_none_null_value_objects(self):
        qs = self.none()
        for obj in self.all():
            if obj.value:
                qs |= self.filter(id=obj.id)
        return qs

    def _get_highest_value_obj(self):
        none_null_values_qs = self.get_none_null_value_objects()
        if none_null_values_qs:
            return sorted(none_null_values_qs, key=lambda l: l.value, reverse=True)[0]
        return None

    def get_total_value(self):
        # The highest value among all certificates is total value
        if self._get_highest_value_obj():
            return float(self._get_highest_value_obj().value)
        return 0

    def get_total_value_label(self):
        # The highest value among all certificates is total value
        if self._get_highest_value_obj():
            return self._get_highest_value_obj().value_label
        return None

    def brief_str(self):
        text = ""
        for certificate in self._chain():
            certificate_text = certificate.brief_str()
            if certificate_text:
                if text != "":
                    text = text + " & "
                text += certificate_text
        return text
