from django.urls import path
from sNeeds.apps.estimation.analyze import views

app_name = "analyze"

urlpatterns = [
    path('<uuid:student_form>/grade-point-average/', views.GradePointAverageChartRetrieveAPIView.as_view(),
         name='grade-point-average-detail'),

    path('<uuid:student_form>/publications-count/', views.PublicationsCountChartRetrieveAPIView.as_view(),
         name='publications-count-detail'),

    path('<uuid:student_form>/publications-type/', views.PublicationTypeChartRetrieveAPIView.as_view(),
         name='publications-type-detail'),

    path('<uuid:student_form>/publications-score/', views.PublicationsScoreChartRetrieveAPIView.as_view(),
         name='publications-score-detail'),

    path('<uuid:student_form>/publications-impact-factor/', views.PublicationImpactFactorChartRetrieveAPIView.as_view(),
         name='publications-impact-factor-detail'),

    path('<uuid:student_form>/powerful-recommendation/', views.PowerfulRecommendationChartRetrieveAPIView.as_view(),
         name='powerful-recommendation-detail'),

    path('<uuid:student_form>/olympiad/', views.OlympiadChartRetrieveAPIView.as_view(),
         name='olympiad-detail'),

    path('<uuid:student_form>/related-work-experience/', views.RelatedWorkExperienceChartRetrieveAPIView.as_view(),
         name='related-work-experience-detail'),

    path('<uuid:student_form>/toefl/', views.ToeflChartRetrieveAPIView.as_view(),
         name='toefl-detail'),

    path('<uuid:student_form>/ielts/', views.IeltsChartRetrieveAPIView.as_view(),
         name='ielts-detail'),

    path('<uuid:student_form>/gmat/', views.GMATChartRetrieveAPIView.as_view(),
         name='gmat-detail'),

    path('<uuid:student_form>/gre-general-writing/', views.GREGeneralWritingChartRetrieveAPIView.as_view(),
         name='gre-general-writing-detail'),

    path('<uuid:student_form>/gre-general-quantitative-and-verbal/',
         views.GREGeneralQuantitativeAndVerbalChartRetrieveAPIView.as_view(),
         name='gre-general-quantitative-and-verbal-detail'),

    path('<uuid:student_form>/gre-subject-total/', views.GRESubjectTotalChartRetrieveAPIView.as_view(),
         name='gre-subject-total-detail'),

    path('<uuid:student_form>/duolingo/', views.DuolingoChartRetrieveAPIView.as_view(),
         name='duolingo-detail'),

    path('<uuid:student_form>/publication/', views.PublicationChartsRetrieveAPIView.as_view(),
         name='publication-charts'),

    path('<uuid:student_form>/language-certificates/', views.LanguageCertificatesRetrieveAPIView,
         name='language-certificates-charts'),

    path('<uuid:student_form>/other/', views.OtherChartsRetrieveAPIView.as_view(),
         name='other-charts'),
]
