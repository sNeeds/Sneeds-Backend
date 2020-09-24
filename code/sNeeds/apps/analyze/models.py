from django.db import models
from enumfields import Enum, EnumField


CHARTS_TITLES = [
    ('grade_point_average',                 'GradePointAverage'),
    ('publications_count',                  'PublicationsCount'),
    ('publications_type',                   'PublicationsType'),
    ('publications_score',                  'PublicationsScore'),
    ('publications_impact_factor',          'PublicationsImpactFactor'),
    ('powerful_recommendation',             'PowerfulRecommendation'),
    ('olympiad',                            'Olympiad'),
    ('related_work_experience',             'RelatedWorkExperience'),
    ('toefl',                               'Toefl'),
    ('ielts',                               'Ielts'),
    ('gmat',                                'GMAT'),
    ('gre_general_writing',                 'GREGeneralWriting'),
    ('gre_general_quantitative_and_verbal', 'GREGeneralQuantitativeAndVerbal'),
    ('gre_subject_total',                   'GRESubjectTotal'),
    ('duolingo',                            'Duolingo'),
]


class ChartTitle(Enum):
    GRADE_POINT_AVERAGE =                  'Grade Point Average'
    PUBLICATIONS_COUNT =                   'Publications Count'
    PUBLICATIONS_TYPE =                    'Publications Type'
    PUBLICATIONS_SCORE =                   'Publications Score'
    PUBLICATIONS_IMPACT_FACTOR =           'Publications Impact Factor'
    POWERFUL_RECOMMENDATION =              'Powerful Recommendation'
    OLYMPIAD =                             'Olympiad'
    RELATED_WORK_EXPERIENCE =              'Related Work Experience'
    TOEFL =                                'Toefl'
    IELTS =                                'Ielts'
    GMAT =                                 'GMAT'
    GRE_GENERAL_WRITING =                  'GRE General Writing'
    GRE_GENERAL_QUANTITATIVE_AND_VERBAL =  'GRE General Quantitative And Verbal'
    GRE_SUBJECT_TOTAL =                    'GRE Subject Total'
    DUOLINGO =                             'Duolingo'


class ChartItemData(models.Model):
    label = models.CharField(
        max_length=128,
    )
    count = models.FloatField(
        default=0,
    )
    chart = models.ForeignKey(
        to='Chart',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['label', 'chart']


class Chart(models.Model):
    # title = models.CharField(
    #     max_length=256,
    #     unique=True,
    # )

    title = EnumField(
        ChartTitle,
        max_length=128,
        unique=True
    )
    created = models.DateTimeField(auto_created=True, auto_now=True)
    # data_number = models.PositiveIntegerField(
    #     default=0,
    # )
    # pass


# class GradePointAverageChart(Chart):
#     #
#     pass
#
#
# class PublicationCountChart(Chart):
#     #
#     pass
#
#
# class PublicationTypeCountChart(Chart):
#     #
#     pass
#
#
# class PublicationsScoreChart(Chart):
#     pass
#
#
# class PublicationsImpactFactorChart(Chart):
#     #
#     pass
#
#
# class PowerfulRecommendationCountChart(Chart):
#     #
#     pass
#
#
# class OlympiadCountChart(Chart):
#     #
#     pass
#
#
# class RelatedWorkExperienceChart(Chart):
#     #
#     pass
#
#
# class ToeflChart(Chart):
#     #
#     pass
#
#
# class IeltsChart(Chart):
#     #
#     pass
#
#
# class GMATChart(Chart):
#     #
#     pass
#
#
# class GREGeneralWritingChart(Chart):
#     #
#     pass
#
#
# class GREGeneralQuantitativeAndVerbalChart(Chart):
#     #
#     pass
#
#
# class GRESubjectTotalChart(Chart):
#     #
#     pass
#
#
# class DuolingoChart(Chart):
#     #
#     pass

