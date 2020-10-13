from django.db import models


class CountryManager(models.Manager):
    def with_active_time_slot_consultants(self):
        from sNeeds.apps.users.consultants.models import StudyInfo

        active_consultant_study_infos = StudyInfo.objects.all().with_active_consultants()
        country_list = list(
            active_consultant_study_infos.values_list('university__country_id', flat=True)
        )
        qs = self.filter(id__in=country_list).exclude(slug="iran")

        return qs


class MajorManager(models.QuerySet):
    def top_nth_parents(self, nth):
        parent_majors = self.none()
        for obj in self._chain():
            parent_majors |= self.filter(id=obj.top_nth_parent(nth).id)

        parent_majors.distinct()
        return parent_majors
