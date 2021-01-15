from django.db.models import Q
from django.http import Http404

from abroadin.base.api.generics import CListAPIView
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.applyprofile.serializers import ApplyProfileSerializer
from abroadin.apps.data.account.models import Major, Country
from abroadin.apps.applyprofile.models import ApplyProfile


class ProfilesListAPIView(CListAPIView):
    lookup_url_kwarg = 'form_id'
    serializer_class = ApplyProfileSerializer

    def get_form(self):
        form_id = self.kwargs[self.lookup_url_kwarg]
        try:
            return StudentDetailedInfo.objects.get(id=form_id)
        except StudentDetailedInfo.DoesNotExist:
            raise Http404

    def get_preferred_apply_country(self):
        return Country.objects.filter(name__iexact="canada")

    def get_want_to_apply_similar_countries(self, want_to_apply):
        want_to_apply_countries_qs = want_to_apply.get_countries_qs()
        want_to_apply_countries_list = want_to_apply_countries_qs.list()

        want_to_apply_universities_qs = want_to_apply.get_universities_qs()
        want_to_apply_universities_countries_list = want_to_apply_universities_qs.get_countries_list()

        similar_destination_countries = want_to_apply_countries_list + want_to_apply_universities_countries_list

        if not similar_destination_countries:
            preferred_apply_country = self.get_preferred_apply_country()
            similar_destination_countries = [preferred_apply_country]

        return similar_destination_countries

    def _filter_around_gpa(self, gpa, profiles):
        qs = profiles.filter

    def _filter_same_want_to_apply_grades(self, profiles, grades):
        profiles_qs = profiles.filter(admission__grade__in=grades)
        return profiles_qs

    def _filter_similar_majors(self, profiles, majors):
        admission_q = Q(admission__major__in=majors)
        education_q = Q(educations__major__in=majors)
        qs = profiles.filter(admission_q | education_q)
        return qs

    def _similar_home_Q(self, profiles):
        return Q()

    def _similar_destination_Q(self, profiles, countries):
        return Q(admission__destination__country__in=countries)

    def _filter_similar_home_and_destination(self, profiles, dest_countries):
        similar_home_q = self._similar_home_Q(profiles)
        similar_destination_q = self._similar_destination_Q(profiles, dest_countries)
        return profiles.filter(similar_home_q | similar_destination_q)

    def get_queryset(self):
        form = self.get_form()

        want_to_apply = form.get_want_to_apply_or_none()
        education_qs = form.education_qs()

        education_major_ids = education_qs.get_majors_id_list()
        education_majors_qs = Major.objects.id_to_qs(education_major_ids)

        want_to_apply_majors_qs = want_to_apply.majors.all()

        form_related_majors = education_majors_qs | want_to_apply_majors_qs
        form_related_majors_parents = form_related_majors.top_nth_parents(3)
        form_related_majors_all_children = form_related_majors_parents.get_all_children_majors()

        grades_want_to_apply = want_to_apply.grades_want_to_apply()
        similar_destination_countries = self.get_want_to_apply_similar_countries(want_to_apply)

        profiles = ApplyProfile.objects.all()
        profiles = self._filter_same_want_to_apply_grades(profiles, grades_want_to_apply)
        profiles = self._filter_similar_majors(profiles, form_related_majors_all_children)
        profiles = self._filter_similar_home_and_destination(profiles, similar_destination_countries)

        return profiles
