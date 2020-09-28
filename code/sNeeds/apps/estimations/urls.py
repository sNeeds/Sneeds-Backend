from django.urls import path

from . import views

app_name = "estimations"

urlpatterns = [
    path('form/<uuid:form_id>/form-comments/', views.FormComments.as_view()),
    path('form/<uuid:form_id>/admission-ranking-chance/', views.AdmissionRankingChance.as_view()),
    path('form/<uuid:form_id>/want-to-apply-chance/', views.WantToApplyChance.as_view()),

    path('import-top-universities/', views.ListUsers.as_view(), ),
]
