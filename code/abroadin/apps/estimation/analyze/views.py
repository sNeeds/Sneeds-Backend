from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from abroadin.utils.custom.views import custom_generic_apiviews as c_generics
from abroadin.apps.estimation.analyze import serializers
from abroadin.apps.estimation.analyze.models import Chart
from abroadin.apps.estimation.analyze.permissions import IsFormOwner


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

        'grade_point_average': {
            'serializer_class': serializers.GradePointAverageChartSerializer,
            'chart_title_enum': Chart.ChartTitle.GRADE_POINT_AVERAGE,
        },
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
