from django.urls import path

from . import views

app_name = "estimation.estimations"

urlpatterns = [
    path('form/<uuid:form_id>/form-comments/', views.FormComments.as_view(), name="form-comments"),
    path('form/<uuid:form_id>/admission-ranking-chance/', views.AdmissionRankingChance.as_view(),
         name="form-admission-ranking-chance"),
    path('form/<uuid:form_id>/want-to-apply-chance/', views.WantToApplyChance.as_view(),
         name="want-to-apply-chance"),
]
