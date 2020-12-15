from django.urls import path

from . import views

urlpatterns = [
    path('form/<uuid:form_id>/similar-profiles/', views.SimilarProfiles.as_view()),
]
