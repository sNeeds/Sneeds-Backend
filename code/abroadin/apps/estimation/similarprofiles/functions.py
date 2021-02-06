from django.db.models import Q

from abroadin.apps.data.account.models import Major
from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.data.account.models import Country


def get_preferred_apply_country():
    return Country.objects.get(name__iexact="canada")


def get_want_to_apply_similar_countries(want_to_apply):
    wta_countries_qs = want_to_apply.get_countries_qs()
    wta_countries_list = wta_countries_qs.list()

    wta_universities_qs = want_to_apply.get_universities_qs()
    wta_universities_countries_list = wta_universities_qs.get_countries_list()
    similar_destination_countries = wta_countries_list + wta_universities_countries_list

    if not similar_destination_countries:
        preferred_apply_country = get_preferred_apply_country()
        similar_destination_countries = [preferred_apply_country]

    return similar_destination_countries


def filter_around_gpa(profiles, gpa, offset):
    assert 0 < offset
    assert offset < 20
    gpa_low = max(0, gpa - offset)
    gpa_high = min(20, gpa + offset)

    high_q = Q(educations__gpa__lte=gpa_high)
    low_q = Q(educations__gpa__gte=gpa_low)

    filtered_profiles = profiles.filter(high_q & low_q)

    return filtered_profiles


def filter_same_want_to_apply_grades(profiles, grades):
    profiles_qs = profiles.filter(admission__grade__in=grades)
    return profiles_qs


def filter_similar_majors(profiles, majors):
    admission_q = Q(admission__major__in=majors)
    education_q = Q(educations__major__in=majors)
    qs = profiles.filter(admission_q | education_q)
    return qs


def similar_home_Q(profiles):
    return Q()


def similar_destination_Q(countries):
    return Q(admission__destination__country__in=countries)


def filter_similar_home_and_destination(profiles, dest_countries):
    similar_home_q = similar_home_Q(profiles)
    similar_destination_q = similar_destination_Q(dest_countries)
    return profiles.filter(similar_home_q | similar_destination_q)


class SimilarProfilesForForm:
    def __init__(self, form):
        self.form = form

    def _extract_form_majors(self):
        want_to_apply = self.form.want_to_apply
        education_qs = self.form.educations.all()

        education_major_ids = education_qs.get_majors_id_list()
        education_majors_qs = Major.objects.id_to_qs(education_major_ids)
        want_to_apply_majors_qs = want_to_apply.majors.all()

        related_majors = education_majors_qs | want_to_apply_majors_qs

        return related_majors

    def _get_related_majors(self, majors):
        majors_parents = majors.top_nth_parents(3)
        related_majors_parents_children = majors_parents.get_all_children_majors()

        return related_majors_parents_children

    def _extract_form_data(self):
        want_to_apply = self.form.want_to_apply
        education_qs = self.form.educations.all()

        grades_want_to_apply = want_to_apply.grades_want_to_apply()
        similar_destination_countries = get_want_to_apply_similar_countries(want_to_apply)
        last_grade_gpa = education_qs.last_education().gpa

        data = {
            "want_to_apply_grades": grades_want_to_apply,
            "destination_countries": similar_destination_countries,
            "last_grade_gpa": last_grade_gpa
        }

        return data

    def _similar_profiles_for_data(self, majors, applied_grades, destination_countries, gpa_around):
        profiles = ApplyProfile.objects.all()
        profiles = filter_around_gpa(profiles, gpa_around, offset=1)
        profiles = filter_same_want_to_apply_grades(profiles, applied_grades)
        profiles = filter_similar_majors(profiles, majors)
        profiles = filter_similar_home_and_destination(profiles, destination_countries)
        profiles = profiles.distinct()

        return profiles

    def find_similar_profiles(self):
        want_to_apply = self.form.want_to_apply
        education_qs = self.form.educations.all()

        form_majors = self._extract_form_majors()
        majors = self._get_related_majors(form_majors)
        applied_grades = want_to_apply.grades_want_to_apply()
        destination_counties = get_want_to_apply_similar_countries(want_to_apply)
        gpa_around = education_qs.last_education().gpa

        profiles = self._similar_profiles_for_data(
            majors, applied_grades, destination_counties, gpa_around
        )
        return profiles
