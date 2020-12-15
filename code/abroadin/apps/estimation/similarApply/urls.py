from django.urls import path

from . import views

app_name = "similar_apply"

urlpatterns = [
    path('form/<uuid:form_id>/similar-universities/', views.SimilarUniversitiesListView.as_view(),
         name="similar-universities"),
]
