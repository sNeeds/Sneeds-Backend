from django.db import models
from django.db.models import Q, F

from ..estimations.classes import ValueRange
from ..estimations.values import VALUES_WITH_ATTRS


class UniversityThroughQuerySetManager(models.QuerySet):
    def get_bachelor(self):
        from abroadin.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.BACHELOR)
        except self.model.DoesNotExist:
            return None

    def get_master(self):
        from abroadin.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.MASTER)
        except self.model.DoesNotExist:
            return None

    def get_phd(self):
        from abroadin.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.PHD)
        except self.model.DoesNotExist:
            return None

    def get_post_doc(self):
        from abroadin.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.POST_DOC)
        except self.model.DoesNotExist:
            return None


class LanguageCertificateQuerysetManager(models.QuerySet):
    def get_from_this_type_or_none(self, certificate_type):
        from abroadin.apps.estimation.form.models import LanguageCertificate
        try:
            return self.get(certificate_type=certificate_type)
        except LanguageCertificate.DoesNotExist:
            return None

    def _get_highest_value_obj(self):
        if self.exists():
            return sorted(self.all(), key=lambda l: l.value, reverse=True)[0]
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


class StudentDetailedInfoManager(models.QuerySet):
    def get_with_value_rank_list(self):
        result = []

        rank = 1
        counter = 0
        prev = self.first()

        for obj in self.all().order_by('-value'):
            counter += 1
            if obj.value != prev.value:
                rank = counter
            prev = obj
            result.append((obj, rank))

        return result

    def add_one_to_rank(self):
        for obj in self.all():
            obj.rank += 1
            obj.save()
