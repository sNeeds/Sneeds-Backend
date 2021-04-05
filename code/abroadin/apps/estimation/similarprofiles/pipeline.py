from .filterings import (BestCaseFiltering,
                         SimilarHomeUniversityExactDestinationCountryFiltering,
                         SimilarHomeUniversityExactDestinationUniversityFiltering, ExactHomeUniversityFiltering,
                         ExactHomeCountryFiltering)
from abroadin.apps.estimation.similarprofiles.taggers import Tagger, SimilarProfilesTagger


class SimilarProfilesPipeline:

    def __init__(self, filterings: iter, tagger: Tagger):
        self.filterings = filterings
        self.tagger = tagger

    def get_querysets(self, profiles, sdi):
        res = {}
        for filtering in self.filterings:
            res[filtering.title] = filtering.filter_and_provide_results_qs(profiles, sdi)
        return res


SimilarProfilesPipelineObject = SimilarProfilesPipeline(
    [
        BestCaseFiltering,
        SimilarHomeUniversityExactDestinationCountryFiltering,
        SimilarHomeUniversityExactDestinationUniversityFiltering,
        ExactHomeUniversityFiltering,
        ExactHomeCountryFiltering,
    ],
    SimilarProfilesTagger,
)
