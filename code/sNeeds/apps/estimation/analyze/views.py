from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from sNeeds.utils.custom.views import custom_generic_apiviews as c_generics
from sNeeds.apps.estimation.analyze import serializers
from sNeeds.apps.estimation.analyze.models import Chart
from sNeeds.apps.estimation.analyze.permissions import IsFormOwner


class BaseChartAPIView(c_generics.BaseGenericAPIView):
    serializer_class = None
    chart_title_enum = None

    permission_classes = [IsFormOwner]

    def get(self, request, *args, **kwargs):
        """Handle get method"""
        if self.kwargs.get('form', None) is None:
            raise NotFound(detail="No from found!")

        try:
            instance = Chart.objects.get(title=self.chart_title_enum)
        except Chart.DoesNotExist:
            raise NotFound(detail="No chart found!")
        serializer = self.serializer_class(
            instance,
            many=False,
            context={'request': request}
        )
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GradePointAverageChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GradePointAverageChartSerializer
    # chart_title = 'grade_point_average'
    chart_title_enum = Chart.ChartTitle.GRADE_POINT_AVERAGE


class PublicationsCountChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationsCountChartSerializer
    # chart_title = 'publications_count'
    chart_title_enum = Chart.ChartTitle.PUBLICATIONS_COUNT


class PublicationTypeChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationTypeChartSerializer
    # chart_title = 'publications_type'
    chart_title_enum = Chart.ChartTitle.PUBLICATION_TYPE


class PublicationsScoreChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationsScoreChartSerializer
    # chart_title = 'publications_score'
    chart_title_enum = Chart.ChartTitle.PUBLICATIONS_SCORE


class PublicationImpactFactorChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PublicationImpactFactorChartSerializer
    # chart_title = 'publications_impact_factor'
    chart_title_enum = Chart.ChartTitle.PUBLICATION_IMPACT_FACTOR


class PowerfulRecommendationChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.PowerfulRecommendationChartSerializer
    # chart_title = 'powerful_recommendation'
    chart_title_enum = Chart.ChartTitle.POWERFUL_RECOMMENDATION


class OlympiadChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.OlympiadChartSerializer
    # chart_title = 'olympiad'
    chart_title_enum = Chart.ChartTitle.OLYMPIAD


class RelatedWorkExperienceChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.RelatedWorkExperienceChartSerializer
    # chart_title = 'related_work_experience'
    chart_title_enum = Chart.ChartTitle.RELATED_WORK_EXPERIENCE


class ToeflChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.ToeflChartSerializer
    # chart_title = 'toefl'
    chart_title_enum = Chart.ChartTitle.TOEFL


class IeltsChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.IeltsChartSerializer
    # chart_title = 'ielts'
    chart_title_enum = Chart.ChartTitle.IELTS


class GMATChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GMATChartSerializer
    # chart_title = 'gmat'
    chart_title_enum = Chart.ChartTitle.GMAT


class GREGeneralWritingChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GREGeneralWritingChartSerializer
    # chart_title = 'gre_general_writing'
    chart_title_enum = Chart.ChartTitle.GRE_GENERAL_WRITING


class GREGeneralQuantitativeAndVerbalChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GREGeneralQuantitativeAndVerbalChartSerializer
    # chart_title = 'gre_general_quantitative_and_verbal'
    chart_title_enum = Chart.ChartTitle.GRE_GENERAL_QUANTITATIVE_AND_VERBAL


class GRESubjectTotalChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.GRESubjectTotalChartSerializer
    chart_title_enum = Chart.ChartTitle.GRE_SUBJECT_TOTAL


class DuolingoChartRetrieveAPIView(BaseChartAPIView):
    serializer_class = serializers.DuolingoChartSerializer
    chart_title_enum = Chart.ChartTitle.DUOLINGO


class BaseChartsAPIView(c_generics.BaseGenericAPIView):
    permission_classes = [IsFormOwner]
    charts_data = {}

    def get(self, request, *args, **kwargs):
        form_id = self.kwargs.get('student_form', None)
        if form_id is None:
            raise NotFound(detail="No from found!")

        response_data = {}

        for chart_title, chart_requirements in self.charts_data.items():
            try:
                instance = Chart.objects.get(title=chart_requirements['chart_title_enum'])
            except Chart.DoesNotExist:
                continue
                # raise NotFound(detail="No chart found!")
            serializer = chart_requirements['serializer_class'](
                instance,
                many=False,
                context={'request': request, 'student_detailed_info': form_id}
            )
            serializer.save()
            response_data[chart_title] = serializer.data

        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )


class PublicationChartsRetrieveAPIView(BaseChartsAPIView):
    charts_data = {
        'publications_count': {'serializer_class': serializers.PublicationsCountChartSerializer,
                               'chart_title_enum': Chart.ChartTitle.PUBLICATIONS_COUNT},

        'publication_type': {'serializer_class': serializers.PublicationTypeChartSerializer,
                             'chart_title_enum': Chart.ChartTitle.PUBLICATION_TYPE},

        'publication_impact_factor': {'serializer_class': serializers.PublicationImpactFactorChartSerializer,
                                      'chart_title_enum': Chart.ChartTitle.PUBLICATION_IMPACT_FACTOR},

        'publications_score': {'serializer_class': serializers.PublicationsScoreChartSerializer,
                               'chart_title_enum': Chart.ChartTitle.PUBLICATIONS_SCORE},
    }


class OtherChartsRetrieveAPIView(BaseChartsAPIView):
    charts_data = {
        'powerful_recommendation': {'serializer_class': serializers.PowerfulRecommendationChartSerializer,
                                    'chart_title_enum': Chart.ChartTitle.POWERFUL_RECOMMENDATION},

        'olympiad': {'serializer_class': serializers.OlympiadChartSerializer,
                     'chart_title_enum': Chart.ChartTitle.OLYMPIAD},

        'related_work_experience': {'serializer_class': serializers.RelatedWorkExperienceChartSerializer,
                                    'chart_title_enum': Chart.ChartTitle.RELATED_WORK_EXPERIENCE},
    }


class LanguageCertificatesRetrieveAPIView(BaseChartsAPIView):
    charts_data = {
        'toefl': {'serializer_class': serializers.ToeflChartSerializer,
                  'chart_title_enum': Chart.ChartTitle.TOEFL},

        'ielts': {'serializer_class': serializers.IeltsChartSerializer,
                  'chart_title_enum': Chart.ChartTitle.IELTS},

        'gmat': {'serializer_class': serializers.GMATChartSerializer,
                 'chart_title_enum': Chart.ChartTitle.GMAT},

        'gre_general_writing': {'serializer_class': serializers.GREGeneralWritingChartSerializer,
                                'chart_title_enum': Chart.ChartTitle.GRE_GENERAL_WRITING},

        'gre_general_quantitative_and_verbal': {
            'serializer_class': serializers.GREGeneralQuantitativeAndVerbalChartSerializer,
            'chart_title_enum': Chart.ChartTitle.GRE_GENERAL_QUANTITATIVE_AND_VERBAL},

        'gre_subject_total': {'serializer_class': serializers.GRESubjectTotalChartSerializer,
                              'chart_title_enum': Chart.ChartTitle.GRE_SUBJECT_TOTAL},

        'duolingo': {'serializer_class': serializers.DuolingoChartSerializer,
                     'chart_title_enum': Chart.ChartTitle.DUOLINGO},
    }
