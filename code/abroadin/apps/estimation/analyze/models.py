from django.db import models
from django.utils.translation import ugettext_lazy as _

from abroadin.apps.estimation.form import models as form_models

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

    def __str__(self):
        return self.title


class ChartItemData(models.Model):
    label = models.CharField(
        max_length=128,
    )
    count = models.FloatField(
        default=0,
    )
    label_rank = models.FloatField(
        default=0
    )
    chart = models.ForeignKey(
        to='Chart',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['label', 'chart']
        ordering = ['chart', 'label_rank']

    def set_rank(self):
        if self.chart.title == Chart.ChartTitle.GRADE_POINT_AVERAGE:
            self.label_rank = form_models.UniversityThrough.get_gpa__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.PUBLICATIONS_COUNT:
            self.label_rank = form_models.Publication.get_publications_count__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.PUBLICATIONS_SCORE:
            self.label_rank = form_models.Publication.get_publications_score__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.PUBLICATION_IMPACT_FACTOR:
            self.label_rank = form_models.Publication.get_impact_factor__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.RELATED_WORK_EXPERIENCE:
            self.label_rank = form_models.StudentDetailedInfo.get_related_work__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.TOEFL:
            self.label_rank = form_models.RegularLanguageCertificate.get_toefl__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.IELTS:
            self.label_rank = form_models.RegularLanguageCertificate.get_ielts__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.GMAT:
            self.label_rank = form_models.GMATCertificate.get_store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.GRE_GENERAL_WRITING:
            self.label_rank = form_models.GREGeneralCertificate.get_writing__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.GRE_GENERAL_QUANTITATIVE_AND_VERBAL:
            self.label_rank = form_models.GREGeneralCertificate.get_q_and_v__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.GRE_SUBJECT_TOTAL:
            self.label_rank = form_models.GRESubjectCertificate.get_total__store_label_rank(self.label)

        if self.chart.title == Chart.ChartTitle.DUOLINGO:
            self.label_rank = form_models.DuolingoCertificate.get_store_label_rank(self.label)
