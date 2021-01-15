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
        parents = self.none()
        for major in self.all():
            major_model = self.model
            top_nth_parent = major.top_nth_parent(nth)
            parents |= major_model.objects.filter(id=top_nth_parent.id)

        parents.distinct()
        return parents

    def id_to_qs(self, ids):
        qs = self.filter(id__in=ids)
        return qs

    def get_all_children_majors(self):
        pass


class UniversityQuerySetManager(GetListManagerMixin, models.QuerySet):
    pass
