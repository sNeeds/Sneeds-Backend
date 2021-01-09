from django.urls import path
from abroadin.apps.estimation.analyze import views

app_name = "estimation.analyze"

urlpatterns = [
    path('<int:form_id>/publication/', views.PublicationChartsRetrieveAPIView.as_view(),
         name='publication-charts'),

    path('<int:form_id>/language-certificates/', views.LanguageCertificatesRetrieveAPIView.as_view(),
         name='language-certificates-charts'),

    path('<int:form_id>/other/', views.OtherChartsRetrieveAPIView.as_view(),
         name='other-charts'),

    # path('akbar/', views.AkbarView.as_view(),
    #      name='other-charts'),
]
