from django.db import models

from abroadin.base.mixins.manager import GetListManagerMixin


class CountryQuerySetManager(GetListManagerMixin, models.QuerySet):
    def with_active_time_slot_consultants(self):
        from abroadin.apps.users.consultants.models import StudyInfo

        active_consultant_study_infos = StudyInfo.objects.all().with_active_consultants()
        country_list = list(
            active_consultant_study_infos.values_list('university__country_id', flat=True)
        )
        qs = self.filter(id__in=country_list).exclude(slug="iran")

        return qs


class MajorManager(models.QuerySet):
    def top_nth_parents(self, nth):
        parent_majors = self.none()
        for major in self.all():
            major_model = self.model
            top_nth_parent = major.top_nth_parent(nth)
            parent_majors |= major_model.objects.filter(id=top_nth_parent.id)

        parent_majors.distinct()
        return parent_majors

    def id_to_qs(self, ids):
        qs = self.filter(id__in=ids)
        return qs


class UniversityQuerySetManager(GetListManagerMixin, models.QuerySet):
    pass
