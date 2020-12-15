from django.urls import path
from abroadin.apps.estimation.analyze import views

app_name = "analyze"

urlpatterns = [
    path('<uuid:form_id>/publication/', views.PublicationChartsRetrieveAPIView.as_view(),
         name='publication-charts'),

    path('<uuid:form_id>/language-certificates/', views.LanguageCertificatesRetrieveAPIView.as_view(),
         name='language-certificates-charts'),

    path('<uuid:form_id>/other/', views.OtherChartsRetrieveAPIView.as_view(),
         name='other-charts'),

    path('akbar/', views.AkbarView.as_view(),
         name='other-charts'),
]
