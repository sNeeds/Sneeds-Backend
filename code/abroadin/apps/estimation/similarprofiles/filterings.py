from django.utils.translation import ngettext_lazy

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.similarprofiles import filters


class Filtering:
    title: str = None
    filters: list = None

    def __init__(self):
        self.results_qs = None

    def filter_and_provide_results_qs(self, profiles, sdi):
        # self.results_qs = profiles
        # for _filter in self.filters:
        #     self.results_qs = _filter.filter(self.results_qs, sdi)
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
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        filters.GeneralSimilarHomeMajorsFilter(),
        filters.GeneralSimilarDestinationMajorsFilter(),
        # filters.VeryGeneralSimilarHomeMajorsFilter(),
        # filters.VeryGeneralSimilarDestinationMajorsFilter(),

        # filters.ExactHomeUniversityFilter(),
        filters.SimilarAndWorseHomeUniversityFilter(),

        filters.SameDestinationFilter(),

        filters.SimilarAndWorseGPAFilter(),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = ngettext_lazy(
            'Find out about %(last_edu_uni)s students who got admission in %(wta_major)s abroad.',
            'Find out about %(last_edu_uni)s students with admissions similar to your desired majors abroad.',
            sdi.want_to_apply.majors.count()
        ) % {
            'last_edu_uni': sdi.last_education.university.name,
            'wta_major': sdi.want_to_apply.majors.first()
        }
        return text


class SimilarHomeUniversityExactDestinationCountryFiltering(Filtering):
    title = 'Dream Country',
    filters = [
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        # filters.MoreSimilarDestinationMajorsFilter(),
        # filters.MoreSimilarHomeMajorsFilter(),
        filters.GeneralSimilarHomeMajorsFilter(),
        filters.GeneralSimilarDestinationMajorsFilter(),
        # filters.VeryGeneralSimilarHomeMajorsFilter(),
        # filters.VeryGeneralSimilarDestinationMajorsFilter(),

        filters.SimilarHomeUniversityFilter(),
        # filters.SimilarAndWorseHomeUniversityFilter(),

        filters.ExactDestinationCountryFilter(),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = ngettext_lazy(
            'Find out about %(last_edu_uni)s students who got admission in %(wta_major)s abroad.',
            'Find out about %(last_edu_uni)s students with admissions similar to your desired majors abroad.',
            sdi.want_to_apply.majors.count()
        ) % {
            'last_edu_uni': sdi.last_education.university.name,
            'wta_major': sdi.want_to_apply.majors.first()
        }
        return text


class SimilarHomeUniversityExactDestinationUniversityFiltering(Filtering):
    title = 'Dream University',
    filters = [
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        # filters.MoreSimilarDestinationMajorsFilter(),
        # filters.MoreSimilarHomeMajorsFilter(),
        filters.GeneralSimilarHomeMajorsFilter(),
        filters.GeneralSimilarDestinationMajorsFilter(),
        # filters.VeryGeneralSimilarHomeMajorsFilter(),
        # filters.VeryGeneralSimilarDestinationMajorsFilter(),

        filters.SimilarHomeUniversityFilter(),
        filters.ExactDestinationUniversityFilter(),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = ngettext_lazy(
            'Find out about %(last_edu_uni)s students who got admission in %(wta_major)s abroad.',
            'Find out about %(last_edu_uni)s students with admissions similar to your desired majors abroad.',
            sdi.want_to_apply.majors.count()
        ) % {
            'last_edu_uni': sdi.last_education.university.name,
            'wta_major': sdi.want_to_apply.majors.first()
        }
        return text


class ExactHomeUniversityFiltering(Filtering):
    title = 'Classmates',
    filters = [
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        # filters.MoreSimilarHomeMajorsFilter(),
        # filters.MoreSimilarDestinationMajorsFilter(),
        filters.GeneralSimilarHomeMajorsFilter(),
        filters.GeneralSimilarDestinationMajorsFilter(),
        # filters.VeryGeneralSimilarHomeMajorsFilter(),
        # filters.VeryGeneralSimilarDestinationMajorsFilter(),
        filters.ExactHomeUniversityFilter(),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = ngettext_lazy(
            'Find out about %(last_edu_uni)s students who got admission in %(wta_major)s abroad.',
            'Find out about %(last_edu_uni)s students with admissions similar to your desired majors abroad.',
            sdi.want_to_apply.majors.count()
        ) % {
            'last_edu_uni': sdi.last_education.university.name,
            'wta_major': sdi.want_to_apply.majors.first()
        }
        return text


class ExactHomeCountryFiltering(Filtering):
    title = 'All',
    filters = [
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        filters.MoreSimilarHomeMajorsFilter(),
        filters.MoreSimilarDestinationMajorsFilter(),
        filters.ExactHomeCountryFilter(),
    ]

    def get_filter_description(self, sdi: StudentDetailedInfo):
        text = ngettext_lazy(
            'Find out about %(last_edu_uni)s students who got admission in %(wta_major)s abroad.',
            'Find out about %(last_edu_uni)s students with admissions similar to your desired majors abroad.',
            sdi.want_to_apply.majors.count()
        ) % {
            'last_edu_uni': sdi.last_education.university.name,
            'wta_major': sdi.want_to_apply.majors.first()
        }
        return text
