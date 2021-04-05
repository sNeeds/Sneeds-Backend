from abroadin.apps.estimation.similarprofiles import filters


class Filtering:

    def __init__(self, title, filters: list):
        self.title = title
        self.filters = filters
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


BestCaseFiltering = Filtering(
    title='Best Case',
    filters=[
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
    ])

SimilarHomeUniversityExactDestinationCountryFiltering = Filtering(
    title='Similar Home University & Exact Destination Country',
    filters=[
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
    ])

SimilarHomeUniversityExactDestinationUniversityFiltering = Filtering(
    title='Similar Home University & Exact Destination University',
    filters=[
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
    ])

ExactHomeUniversityFiltering = Filtering(
    title='Exact Home University',
    filters=[
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        # filters.MoreSimilarHomeMajorsFilter(),
        # filters.MoreSimilarDestinationMajorsFilter(),
        filters.GeneralSimilarHomeMajorsFilter(),
        filters.GeneralSimilarDestinationMajorsFilter(),
        # filters.VeryGeneralSimilarHomeMajorsFilter(),
        # filters.VeryGeneralSimilarDestinationMajorsFilter(),
        filters.ExactHomeUniversityFilter(),
    ])

ExactHomeCountryFiltering = Filtering(
    title='Exact Home Country',
    filters=[
        # filters.ExactHomeMajorsFilter(),
        # filters.ExactDestinationMajorsFilter(),
        filters.MoreSimilarHomeMajorsFilter(),
        filters.MoreSimilarDestinationMajorsFilter(),
        filters.ExactHomeCountryFilter(),
    ])


