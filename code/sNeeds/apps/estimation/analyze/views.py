from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from sNeeds.utils.custom.views import custom_generic_apiviews as c_generics
from sNeeds.apps.estimation.analyze import serializers
from sNeeds.apps.estimation.analyze.models import Chart


class BaseChartAPIView(c_generics.BaseGenericAPIView):

    serializer_class = None
    chart_title_enum = None

    def get(self, request, *args, **kwargs):
        """Handle get method"""
        try:
            instance = Chart.objects.get(title=self.chart_title_enum)
        except Chart.DoesNotExist:
            raise NotFound(detail="No chart found!")
        serializer = self.serializer_class(instance, many=False, context={'request': request})
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GradePointAverageChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GradePointAverageChartSerializer
    # chart_title = 'grade_point_average'
    chart_title_enum = Chart.ChartTitleChoices.GRADE_POINT_AVERAGE


class PublicationsCountChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationsCountChartSerializer
    # chart_title = 'publications_count'
    chart_title_enum = Chart.ChartTitleChoices.PUBLICATIONS_COUNT


class PublicationTypeChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationTypeChartSerializer
    # chart_title = 'publications_type'
    chart_title_enum = Chart.ChartTitleChoices.PUBLICATION_TYPE


class PublicationsScoreChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationsScoreChartSerializer
    # chart_title = 'publications_score'
    chart_title_enum = Chart.ChartTitleChoices.PUBLICATIONS_SCORE


class PublicationImpactFactorChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationImpactFactorChartSerializer
    # chart_title = 'publications_impact_factor'
    chart_title_enum = Chart.ChartTitleChoices.PUBLICATION_IMPACT_FACTOR


class PowerfulRecommendationChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PowerfulRecommendationChartSerializer
    # chart_title = 'powerful_recommendation'
    chart_title_enum = Chart.ChartTitleChoices.POWERFUL_RECOMMENDATION


class OlympiadChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.OlympiadChartSerializer
    # chart_title = 'olympiad'
    chart_title_enum = Chart.ChartTitleChoices.OLYMPIAD


class RelatedWorkExperienceChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.RelatedWorkExperienceChartSerializer
    # chart_title = 'related_work_experience'
    chart_title_enum = Chart.ChartTitleChoices.RELATED_WORK_EXPERIENCE


class ToeflChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.ToeflChartSerializer
    # chart_title = 'toefl'
    chart_title_enum = Chart.ChartTitleChoices.TOEFL


class IeltsChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.IeltsChartSerializer
    # chart_title = 'ielts'
    chart_title_enum = Chart.ChartTitleChoices.IELTS


class GMATChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GMATChartSerializer
    # chart_title = 'gmat'
    chart_title_enum = Chart.ChartTitleChoices.GMAT


class GREGeneralWritingChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GREGeneralWritingChartSerializer
    # chart_title = 'gre_general_writing'
    chart_title_enum = Chart.ChartTitleChoices.GRE_GENERAL_WRITING


class GREGeneralQuantitativeAndVerbalChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GREGeneralQuantitativeAndVerbalChartSerializer
    # chart_title = 'gre_general_quantitative_and_verbal'
    chart_title_enum = Chart.ChartTitleChoices.GRE_GENERAL_QUANTITATIVE_AND_VERBAL


class GRESubjectTotalChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GRESubjectTotalChartSerializer
    # chart_title = 'gre_subject_total'
    chart_title_enum = Chart.ChartTitleChoices.GRE_SUBJECT_TOTAL


class DuolingoChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.DuolingoChartSerializer
    # chart_title = 'duolingo'
    chart_title_enum = Chart.ChartTitleChoices.DUOLINGO
