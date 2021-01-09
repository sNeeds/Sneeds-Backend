from django.urls import path

from . import views

urlpatterns = [
    path('form/<int:form_id>/similar-profiles/', views.SimilarProfiles.as_view()),
]
