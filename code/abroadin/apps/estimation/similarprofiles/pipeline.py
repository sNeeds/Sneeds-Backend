from .filterings import (BestCaseFiltering,
                         SimilarHomeUniversityExactDestinationCountryFiltering,
                         SimilarHomeUniversityExactDestinationUniversityFiltering, ExactHomeUniversityFiltering,
                         ExactHomeCountryFiltering)

from abroadin.apps.estimation.similarprofiles.taggers import Tagger, SimilarProfilesTagger
from ..form.exceptions import SDIDefectException


class SimilarProfilesPipeline:

    def __init__(self, filterings: iter, tagger: Tagger):
        self.filterings = filterings
        self.tagger = tagger

    def get_filter_results(self, profiles, sdi):
        res = []
        for filtering in self.filterings:
            try:
                res.append({'title': filtering.title,
                            'description': filtering.get_filter_description(sdi),
                            # 'qs': filtering.filter_and_provide_results_qs(profiles, sdi),
                            'qs': None,
                            'failure': False,
                            'failure_text': None,
                            'failure_front_code': None,
                            'ids': filtering.filter_and_provide_results_qs(profiles, sdi).only('id').values_list('id', flat=True),
                            })
            except SDIDefectException as e:
                res.append({'title': filtering.title,
                            'description': filtering.get_filter_description(sdi),
                            'qs': None,
                            'failure': True,
                            'failure_text': e.pretty_message,
                            'failure_front_code': e.front_code,
                            'ids': [],
                            })
        return res


SimilarProfilesPipelineObject = SimilarProfilesPipeline(
    [
        BestCaseFiltering(),
        SimilarHomeUniversityExactDestinationCountryFiltering(),
        SimilarHomeUniversityExactDestinationUniversityFiltering(),
        ExactHomeUniversityFiltering(),
        ExactHomeCountryFiltering(),
    ],
    SimilarProfilesTagger,
)
