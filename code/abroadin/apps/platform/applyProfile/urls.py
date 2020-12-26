from django.urls import path

from . import views

app_name = "platform.applyProfile"

urlpatterns = [
    path('apply_profiles/', views.ApplyProfileAPIView.as_view(), name='apply-profile-list'),
    # path('apply_profiles/<id:int>/'),
]
