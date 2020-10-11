from django.db import models
from django.db.models import Q, F

from ..estimations.classes import ValueRange
from ..estimations.values import VALUES_WITH_LABELS


class UniversityThroughQuerySetManager(models.QuerySet):
    def get_bachelor(self):
        from sNeeds.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.BACHELOR)
        except self.model.DoesNotExist:
            return None

    def get_master(self):
        from sNeeds.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.MASTER)
        except self.model.DoesNotExist:
            return None

    def get_phd(self):
        from sNeeds.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.PHD)
        except self.model.DoesNotExist:
            return None

    def get_post_doc(self):
        from sNeeds.apps.estimation.form.models import GradeChoices
        try:
            return self.all().get(grade=GradeChoices.POST_DOC)
        except self.model.DoesNotExist:
            return None


class LanguageCertificateQuerysetManager(models.QuerySet):
    def get_IELTS(self):
        from sNeeds.apps.estimation.form.models import LanguageCertificate
        return self.filter(Q(certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL)
                           | Q(certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC))

    def get_TOEFL(self):
        from sNeeds.apps.estimation.form.models import LanguageCertificate
        return self.filter(certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL)

    def get_GRE(self):
        from sNeeds.apps.estimation.form.models import LanguageCertificate
        return self.filter(certificate_type=LanguageCertificate.LanguageCertificateType.GRE)

    def get_Duolingo(self):
        from sNeeds.apps.estimation.form.models import LanguageCertificate
        return self.filter(certificate_type=LanguageCertificate.LanguageCertificateType.DUOLINGO)

    def _get_highest_value_obj(self):
        return self.all().order_by(F('value').desc(nulls_last=True)).first()

    def get_total_value(self):
        # The highest value among all certificates is total value
        if self._get_highest_value_obj():
            return self._get_highest_value_obj().compute_value()[0]
        return 0

    def get_total_value_str(self):
        # The highest value among all certificates is total value
        if self._get_highest_value_obj():
            return self._get_highest_value_obj().compute_value()[1]
        return None


class PublicationQuerySetManager(models.QuerySet):
    def qs_total_value(self):
        qs = self.all().order_by('value')
        total_val = 0

        counter = 0
        for p in qs:
            total_val += max((p.value - counter), 0)
            counter += 0.3

        total_val = max(total_val, 1)
        return total_val

    def qs_total_value_str(self):
        value_range = ValueRange(VALUES_WITH_LABELS["publication_qs"])
        label = value_range.find_value_attrs(self.qs_total_value(), 'label')

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
