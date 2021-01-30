from django.urls import path

from . import views

app_name = "applyprofile"

urlpatterns = [
    path('apply-profiles/', views.ApplyProfileAPIView.as_view(), name='apply-profile-list'),
    path('apply-profiles/<int:id>/', views.ApplyProfileDetailAPIView.as_view(), name='apply-profile-detail'),
]
