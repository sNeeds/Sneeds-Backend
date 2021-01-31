from django.db.models import Q

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


def filter_around_gpa(profiles):
    # Todo : implement
    return profiles


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
