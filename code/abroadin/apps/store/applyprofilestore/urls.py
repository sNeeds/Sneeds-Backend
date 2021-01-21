from django.urls import path
from . import views


urlpatterns = [
    path('apply-profile-group-store/', views.ApplyProfileGroupListView.as_view(),
         name='apply-profile-group-store-list'),
    path('apply-profile-group-store/<int:id>/', views.ApplyProfileGroupDetailView.as_view(),
         name='apply-profile-group-store-detail'),
]
