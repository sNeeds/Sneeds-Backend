from django.db import models, transaction
from django.db.models import Q, F


class UniversityThroughQuerySetManager(models.QuerySet):
    def get_bachelor(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().get(grade=Grade.BACHELOR)
        except self.model.DoesNotExist:
            return None

    def get_master(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().get(grade=Grade.MASTER)
        except self.model.DoesNotExist:
            return None

    def get_phd(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().get(grade=Grade.PHD)
        except self.model.DoesNotExist:
            return None

    def get_post_doc(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().get(grade=Grade.POST_DOC)
        except self.model.DoesNotExist:
            return None


class LanguageCertificateQuerysetManager(models.QuerySet):
    def get_IELTS(self):
        from sNeeds.apps.account.models import LanguageCertificateType
        return self.filter(Q(certificate_type=LanguageCertificateType.IELTS_GENERAL)
                           | Q(certificate_type=LanguageCertificateType.IELTS_ACADEMIC))

    def get_TOEFL(self):
        from sNeeds.apps.account.models import LanguageCertificateType
        return self.filter(certificate_type=LanguageCertificateType.TOEFL)

    def get_GRE(self):
        from sNeeds.apps.account.models import LanguageCertificateType
        return self.filter(certificate_type=LanguageCertificateType.GRE)

    def get_Duolingo(self):
        from sNeeds.apps.account.models import LanguageCertificateType
        return self.filter(certificate_type=LanguageCertificateType.DUOLINGO)

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


class CountryManager(models.Manager):
    def with_active_time_slot_consultants(self):
        from sNeeds.apps.consultants.models import StudyInfo

        active_consultant_study_infos = StudyInfo.objects.all().with_active_consultants()
        country_list = list(
            active_consultant_study_infos.values_list('university__country_id', flat=True)
        )
        qs = self.filter(id__in=country_list).exclude(slug="iran")

        return qs


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
        total_value = self.qs_total_value()
        total_value_str = None

        if 0.95 <= total_value:
            total_value_str = "A+"
        elif 0.75 <= total_value < 0.95:
            total_value_str = "A"
        elif 0.6 <= total_value < 0.75:
            total_value_str = "B+"
        elif 0.5 <= total_value < 0.6:
            total_value_str = "B"
        elif 0.4 <= total_value < 0.5:
            total_value_str = "C+"
        elif 0.3 <= total_value < 0.4:
            total_value_str = "C"
        elif total_value < 0.3:
            total_value_str = "D"

        return total_value_str


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