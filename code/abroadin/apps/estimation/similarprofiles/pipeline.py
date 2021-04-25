from .filterings import (BestCaseFiltering,
                         SimilarHomeUniversityExactDestinationCountryFiltering,
                         SimilarHomeUniversityExactDestinationUniversityFiltering, ExactHomeUniversityFiltering,
                         ExactHomeCountryFiltering)
from abroadin.apps.estimation.similarprofiles.taggers import Tagger, SimilarProfilesTagger
from ..form.exceptions import SDIDefectException
from ...data.globaldata.models import Major


class SimilarProfilesPipeline:

    def __init__(self, filterings: iter, tagger: Tagger):
        self.filterings = filterings
        self.tagger = tagger

    def get_filter_results(self, profiles, sdi):
        res = []
        for filtering in self.filterings:
            try:
                # print('sdi last edu major:', sdi.last_education.major.name, '\n',
                #       'sdi last edu parent major:', sdi.last_education.major.parent.name, '\n',
                #       'sdi last edu children major:', Major.objects.filter(parent=sdi.last_education.major),
                #       # Major.objects.filter(parent__id__in=sdi.educations.all().values_list('major__id', flat=True)).values_list('name', flat=True)
                #       )
                print( filtering.title)
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
