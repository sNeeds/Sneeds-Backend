from django.db import models


class CountryManager(models.QuerySet):
    def with_active_time_slot_consultants(self):
        from abroadin.apps.users.consultants.models import StudyInfo

        active_consultant_study_infos = StudyInfo.objects.all().with_active_consultants()
        country_list = list(
            active_consultant_study_infos.values_list('university__country_id', flat=True)
        )
        qs = self.filter(id__in=country_list).exclude(slug="iran")

        return qs

    def list(self):
        return [obj for obj in self._chain()]


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
        return_qs = self.all()
        for obj in self.all():
            return_qs |= obj.get_all_children_majors()
        return return_qs


class UniversityManager(models.QuerySet):
    def get_countries_list(self):
        Country = self.model._meta.get_field('country').remote_field.model
        country_ids = self.values_list('country', flat=True)
        countries_qs = Country.objects.filter(id__in=country_ids)
        return list(countries_qs)

    def list(self):
        return list(self.all())
