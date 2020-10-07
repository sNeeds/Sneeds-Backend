from django.db import models
from django.utils.translation import ugettext_lazy as _

CHARTS_TITLES = [
    ('grade_point_average', 'GradePointAverage'),
    ('publications_count', 'PublicationsCount'),
    ('publications_type', 'PublicationsType'),
    ('publications_score', 'PublicationsScore'),
    ('publications_impact_factor', 'PublicationsImpactFactor'),
    ('powerful_recommendation', 'PowerfulRecommendation'),
    ('olympiad', 'Olympiad'),
    ('related_work_experience', 'RelatedWorkExperience'),
    ('toefl', 'Toefl'),
    ('ielts', 'Ielts'),
    ('gmat', 'GMAT'),
    ('gre_general_writing', 'GREGeneralWriting'),
    ('gre_general_quantitative_and_verbal', 'GREGeneralQuantitativeAndVerbal'),
    ('gre_subject_total', 'GRESubjectTotal'),
    ('duolingo', 'Duolingo'),
]



def get_chart_titles_choices():
    choices = []
    for choice in Chart.ChartTitle.choices:
        choices.append((choice.value, choice.name))
    return choices


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
    class ChartTitle(models.TextChoices):
        GRADE_POINT_AVERAGE = 'Grade Point Average', _('Grade Point Average')
        PUBLICATIONS_COUNT = 'Publications Count', _('Publications Count')
        PUBLICATION_TYPE = 'Publication Type', _('Publication Type')
        PUBLICATIONS_SCORE = 'Publications Score', _('Publications Score')
        PUBLICATION_IMPACT_FACTOR = 'Publication Impact Factor', _('Publication Impact Factor')
        POWERFUL_RECOMMENDATION = 'Powerful Recommendation', _('Powerful Recommendation')
        OLYMPIAD = 'Olympiad', _('Olympiad')
        RELATED_WORK_EXPERIENCE = 'Related Work Experience', _('Related Work Experience')
        TOEFL = 'Toefl', _('Toefl')
        IELTS = 'Ielts', _('Ielts')
        GMAT = 'GMAT', _('GMAT')
        GRE_GENERAL_WRITING = 'GRE General Writing', _('GRE General Writing')
        GRE_GENERAL_QUANTITATIVE_AND_VERBAL = 'GRE General Quantitative And Verbal', _(
            'GRE General Quantitative And Verbal')
        GRE_SUBJECT_TOTAL = 'GRE Subject Total', _('GRE Subject Total')
        DUOLINGO = 'Duolingo', _('Duolingo')

    title = models.CharField(
        choices=ChartTitle.choices,
        max_length=128,
        unique=True
    )
    created = models.DateTimeField(auto_created=True, auto_now=True)

    # data_number = models.PositiveIntegerField(
    #     default=0,
    # )
    # pass

    def __str__(self):
        return self.title
