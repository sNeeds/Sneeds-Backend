import itertools
import random

from .filterings import (BestCaseFiltering,
                         SimilarHomeUniversityExactDestinationCountryFiltering,
                         SimilarHomeUniversityExactDestinationUniversityFiltering, ExactHomeUniversityFiltering,
                         ExactHomeCountryFiltering)

from abroadin.apps.estimation.similarprofiles.taggers import Tagger, SimilarProfilesTagger
from ..form.exceptions import SDIDefectException


class SimilarProfilesPipeline:
    max_result_size = 10

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
                            'ids': self.prepare_suitable_result_ids(filtering, profiles, sdi),
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

    def prepare_suitable_result_ids(self, filtering, profiles, sdi):
        normal_ids = filtering.normal_filter_and_provide_results_qs(profiles, sdi) \
            .only('id').values_list('id', flat=True)
        normal_ids = set(normal_ids)

        if len(normal_ids) <= self.max_result_size:
            return normal_ids

        strict_ids = filtering.strict_filter_and_provide_results_qs(profiles, sdi) \
            .only('id').values_list('id', flat=True)
        strict_ids = set(strict_ids)

        if len(strict_ids) <= self.max_result_size:
            return strict_ids

        return set(itertools.islice(normal_ids, self.max_result_size))


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
