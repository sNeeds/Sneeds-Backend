from django.urls import path
from . import views

app_name = 'store.applyprofilestore'


urlpatterns = [
    path('apply-profile-groups/', views.ApplyProfileGroupListView.as_view(),
         name='apply-profile-group-list'),
    path('apply-profile-groups/<int:id>/', views.ApplyProfileGroupDetailView.as_view(),
         name='apply-profile-group-detail'),

    path('sold-apply-profile-groups/', views.SoldApplyProfileGroupListView.as_view(),
         name='sold-apply-profile-group-list'),
    path('sold-apply-profile-groups/<int:id>/', views.SoldApplyProfileGroupDetailView.as_view(),
         name='sold-apply-profile-group-detail'),
]
