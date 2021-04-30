from django.utils.translation import ngettext_lazy

from abroadin.apps.estimation.form.exceptions import SDIEducationLeakage, SDIWantToApplyUniversityAndCountryLeakage, \
    SDIWantToApplyCountryLeakage, SDIWantToApplyMajorLeakage, SDIWantToApplyUniversityLeakage
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles import filters
from abroadin.apps.estimation.similarprofiles.constraints import SIMILAR_GPA_OFFSET


class Filtering:
    title: str = None
    filters: list = None

    def __init__(self):
        self.results_qs = None

    def filter_and_provide_results_qs(self, profiles, sdi):
        if self.filters:
            final_query = self.filters.pop().get_query(profiles, sdi)
            for _filter in self.filters:
                final_query = final_query & _filter.get_query(profiles, sdi)
            return profiles.filter(final_query)
        return profiles

    def get_filter_description(self, sdi: StudentDetailedInfo):
        raise NotImplementedError


class BestCaseFiltering(Filtering):
    title = 'Best Matches Ancestors',
    filters = [
        filters.MoreGeneralSimilarHomeMajorsFilter(),
        filters.MoreGeneralSimilarDestinationMajorsFilter(),

        filters.ExactHomeUniversityFilter(raise_defect_exception=True,
                                          accepted_defect_exceptions=[SDIEducationLeakage]),

        filters.SameDestinationFilter(raise_defect_exception=True,
                                      accepted_defect_exceptions=[SDIWantToApplyUniversityAndCountryLeakage]),

        filters.SimilarAndWorseGPAFilter(raise_defect_exception=True,
                                         accepted_defect_exceptions=[SDIEducationLeakage]),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = 'Find out about your university fellows with admissions close to your' \
               ' desired majors and universities with a GPA under your gpa.'
        wta_majors = list(sdi.want_to_apply.majors.values_list('name', flat=True))
        wta_universities = list(sdi.want_to_apply.universities.values_list('name', flat=True))

        if len(wta_majors) == 1:
            text = ngettext_lazy(
                'Find out about %(last_edu_uni)s students admitted to %(wta_major)s'
                ' at %(wta_university)s with a GPA under %(gpa_upper_bound)d.',

                'Find out about %(last_edu_uni)s students admitted to %(wta_major)s'
                ' with a GPA under %(gpa_upper_bound)d based on your desired universities.',
                len(wta_universities)
            ) % {
                       'last_edu_uni': sdi.last_education.university.name,
                       'wta_major': wta_majors.pop().strip(),
                       'wta_university': wta_universities.pop(),
                       'gpa_upper_bound': sdi.last_education.gpa + SIMILAR_GPA_OFFSET,
                   }

        if len(wta_majors) > 1:
            text = ngettext_lazy(
                'Find out about %(last_edu_uni)s students admitted to your desired majors'
                ' at %(wta_university)s with a GPA under %(gpa_upper_bound)d.'
                'Find out about %(last_edu_uni)s students with admissions close to your'
                ' desired majors and universities with a GPA under %(gpa_upper_bound)d.',
                len(wta_universities)
            ) % {
                       'last_edu_uni': sdi.last_education.university.name,
                       'wta_university': wta_universities.pop(),
                       'gpa_upper_bound': sdi.last_education.gpa + SIMILAR_GPA_OFFSET,
                   }
        return text


class SimilarHomeUniversityExactDestinationCountryFiltering(Filtering):
    title = 'Dream Country',
    filters = [
        filters.MoreGeneralSimilarHomeMajorsFilter(raise_defect_exception=True,
                                                   accepted_defect_exceptions=[SDIEducationLeakage]),
        filters.MoreGeneralSimilarDestinationMajorsFilter(raise_defect_exception=True,
                                                          accepted_defect_exceptions=[SDIWantToApplyMajorLeakage]),

        filters.SimilarHomeUniversityFilter(),
        # filters.SimilarAndWorseHomeUniversityFilter(),

        filters.ExactDestinationCountryFilter(raise_defect_exception=True,
                                              accepted_defect_exceptions=[SDIWantToApplyUniversityAndCountryLeakage]),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = 'Find out about students admitted to your desired countries and desired majors' \
               ' from universities with rankings close to your education university.'

        wta_majors = list(sdi.want_to_apply.majors.values_list('name', flat=True))
        wta_countries = list(sdi.want_to_apply.countries.values_list('name', flat=True))
        if len(wta_majors) == 1:
            text = ngettext_lazy(
                'Find out about %(wta_major)s students admitted to %(wta_country)s from universities'
                ' with rankings close to %(last_edu_uni)s.',

                'Find out about %(wta_major)s students admitted to your desired countries from universities'
                ' with rankings close to %(last_edu_uni)s.',
                len(wta_countries)
            ) % {
                       'last_edu_uni': sdi.last_education.university.name,
                       'wta_major': wta_majors.pop().strip(),
                       'wta_country': wta_countries.pop(),
                   }

        if len(wta_majors) > 1:
            text = ngettext_lazy(
                'Find out about students admitted to your desired majors in %(wta_country)s from universities'
                ' with rankings close to %(last_edu_uni)s.',

                'Find out about students admitted to your desired countries and desired majors from universities'
                ' with rankings close to %(last_edu_uni)s.',
                len(wta_countries)
            ) % {
                       'last_edu_uni': sdi.last_education.university.name,
                       'wta_country': wta_countries.pop(),
                   }

        return text


class SimilarHomeUniversityExactDestinationUniversityFiltering(Filtering):
    title = 'Dream University',
    filters = [
        filters.MoreGeneralSimilarHomeMajorsFilter(raise_defect_exception=True,
                                                   accepted_defect_exceptions=[SDIEducationLeakage]),
        filters.MoreGeneralSimilarDestinationMajorsFilter(raise_defect_exception=True,
                                                          accepted_defect_exceptions=[SDIWantToApplyMajorLeakage]),

        filters.SimilarHomeUniversityFilter(raise_defect_exception=True,
                                            accepted_defect_exceptions=[SDIEducationLeakage]),
        filters.ExactDestinationUniversityFilter(raise_defect_exception=True,
                                                 accepted_defect_exceptions=[SDIWantToApplyUniversityLeakage]),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = 'Find out about students with admissions close to your desired majors and universities' \
               ' from universities with rankings close to your education university.'

        wta_majors = list(sdi.want_to_apply.majors.values_list('name', flat=True))
        wta_universities = list(sdi.want_to_apply.universities.values_list('name', flat=True))

        if len(wta_majors) == 1:
            text = ngettext_lazy(
                'Find out about %(wta_major)s students admitted to %(wta_university)s from universities'
                ' with rankings close to %(last_edu_uni)s.',
                'Find out about %(wta_major)s students with admissions in your desired universities from universities'
                ' with rankings close to %(last_edu_uni)s.',
                len(wta_universities)
            ) % {
                       'wta_major': wta_majors.pop().strip(),
                       'wta_university': wta_universities.pop(),
                       'last_edu_uni': sdi.last_education.university.name,
                   }

        if len(wta_majors) > 1:
            text = ngettext_lazy(
                'Find out about students admitted to your desired majors in %(wta_university)s'
                ' from universities with rankings close to %(last_edu_uni)s.',
                'Find out about students with admissions close to your desired majors and universities'
                ' from universities with rankings close to %(last_edu_uni)s.',
                len(wta_universities)
            ) % {
                       'wta_university': wta_universities.pop(),
                       'last_edu_uni': sdi.last_education.university.name,
                   }

        return text


class ExactHomeUniversityFiltering(Filtering):
    title = 'Classmates',
    filters = [
        filters.GeneralSimilarHomeMajorsFilter(raise_defect_exception=True,
                                               accepted_defect_exceptions=[SDIEducationLeakage]),
        filters.GeneralSimilarDestinationMajorsFilter(raise_defect_exception=True,
                                                      accepted_defect_exceptions=[SDIWantToApplyMajorLeakage]),
        filters.ExactHomeUniversityFilter(raise_defect_exception=True,
                                          accepted_defect_exceptions=[SDIEducationLeakage]),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = 'Find out about your university fellows with admissions similar to your desired majors abroad.'

        wta_majors = list(sdi.want_to_apply.majors.values_list('name', flat=True))
        if len(wta_majors) > 0:
            text = ngettext_lazy(
                'Find out about %(last_edu_uni)s students who got admission in %(wta_major)s abroad.',
                'Find out about %(last_edu_uni)s students with admissions similar to your desired majors abroad.',
                len(wta_majors)
            ) % {
                       'last_edu_uni': sdi.last_education.university.name,
                       'wta_major': wta_majors.pop().strip()
                   }
        return text


class ExactHomeCountryFiltering(Filtering):
    title = 'All',
    filters = [
        filters.VerySimilarHomeMajorsFilter(raise_defect_exception=True,
                                            accepted_defect_exceptions=[SDIEducationLeakage]),

        filters.VerySimilarDestinationMajorsFilter(raise_defect_exception=True,
                                                   accepted_defect_exceptions=[SDIWantToApplyMajorLeakage]),
        filters.ExactHomeCountryFilter(),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = 'Find out about your compatriot students admitted abroad, close to your desired majors.'

        wta_majors = list(sdi.want_to_apply.majors.values_list('name', flat=True))
        if len(wta_majors) > 0:
            text = ngettext_lazy(
                'Find out about %(last_edu_country_demonym)s students admitted abroad to %(wta_major)s',
                'Find out about %(last_edu_country_demonym)s students admitted abroad, close to your desired majors.',
                len(wta_majors)
            ) % {
                       'last_edu_country_demonym': sdi.last_education.university.country.demonym.strip(),
                       'wta_major': wta_majors.pop().strip(),
                   }
        return text
