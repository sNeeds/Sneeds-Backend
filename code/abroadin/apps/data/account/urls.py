from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<str:slug>/', views.CountryDetail.as_view(), name="country-detail"),

    path('universities/', views.UniversityList.as_view(), name="university-list"),
    path('universities/<int:id>/', views.UniversityDetail.as_view(), name="university-detail"),
    path('form-universities/', views.UniversityForFormList.as_view(), name='form-university-list'),

    path('field-of-studies/', views.MajorList.as_view(), name="field-of-study-list"),
    path('field-of-studies/<int:id>/', views.MajorDetail.as_view(), name="field-of-study-detail"),
    path('form-field-of-studies/', views.MajorForFormList.as_view(), name='form-field-of-study-list'),
]
