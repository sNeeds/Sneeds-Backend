from django.urls import path

from . import views

app_name = "estimation.similarprofiles"

urlpatterns = [
    path('form/<int:form_id>/similar-profiles/', views.ProfilesListAPIView.as_view(),  name='similar-profiles-list'),
    path('form/<int:form_id>/similar-profiles-v2/', views.ProfilesListAPIViewVersion2.as_view(),
         name='similar-profiles-list-v2'),
    path('hello/', views.ProfilesListAPIView.as_view(),  name='profiles-list'),
]
