from django.urls import path

from . import views

app_name = "estimation.similarprofiles"

urlpatterns = [
    path('form/<int:form_id>/similar-profiles/', views.ProfilesListAPIView.as_view(),  name='profiles-list'),
]
