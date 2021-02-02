from django.db.models import Q

from abroadin.apps.data.account.models import Major
from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.data.account.models import Country


def get_preferred_apply_country():
    return Country.objects.get(name__iexact="canada")


def get_want_to_apply_similar_countries(want_to_apply):
    want_to_apply_countries_qs = want_to_apply.get_countries_qs()
    want_to_apply_countries_list = want_to_apply_countries_qs.list()

    want_to_apply_universities_qs = want_to_apply.get_universities_qs()
    want_to_apply_universities_countries_list = want_to_apply_universities_qs.get_countries_list()
    similar_destination_countries = want_to_apply_countries_list + want_to_apply_universities_countries_list

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


def similar_profiles_for_form(form):
    print(1)
    want_to_apply = form.get_want_to_apply_or_none()
    print(2)
    education_qs = form.education_qs()
    print(3)

    education_major_ids = education_qs.get_majors_id_list()
    print(4)
    education_majors_qs = Major.objects.id_to_qs(education_major_ids)
    print(5)

    want_to_apply_majors_qs = want_to_apply.majors.all()
    print(6)

    form_related_majors = education_majors_qs | want_to_apply_majors_qs
    print(7)
    form_related_majors_parents = form_related_majors.top_nth_parents(2)
    print(8)
    form_related_majors_all_children = form_related_majors_parents.get_all_children_majors()
    print(9)

    grades_want_to_apply = want_to_apply.grades_want_to_apply()
    print(10)
    similar_destination_countries = get_want_to_apply_similar_countries(want_to_apply)
    print(11)

    profiles = ApplyProfile.objects.all()
    print(12)
    profiles = filter_around_gpa(profiles, education_qs.last_education().gpa, offset=1)
    print(12.5)
    profiles = filter_same_want_to_apply_grades(profiles, grades_want_to_apply)
    print(13)
    profiles = filter_similar_majors(profiles, form_related_majors_all_children)
    print(14)
    profiles = filter_similar_home_and_destination(profiles, similar_destination_countries)
    print(15)

    profiles = profiles.distinct()
    print(16)
    return profiles
