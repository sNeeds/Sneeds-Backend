from django.urls import path

import sNeeds.apps.consultants.views
from . import views

app_name = "account"


urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<str:slug>/', views.CountryDetail.as_view(), name="country-detail"),

    path('universities/', views.UniversityList.as_view(), name="university-list"),
    path('universities/<int:id>/', views.UniversityDetail.as_view(), name="university-detail"),

    path('field-of-studies/', views.FieldOfStudyList.as_view(), name="field-of-study-list"),
    path('field-of-studies/<int:id>/', views.FieldOfStudyDetail.as_view(), name="field-of-study-detail"),

    path('consultant-profiles/', sNeeds.apps.consultants.views.ConsultantProfileList.as_view(),
         name="consultant-profile-list"),
    path('consultant-profiles/<str:slug>/', sNeeds.apps.consultants.views.ConsultantProfileDetail.as_view(),
         name="consultant-profile-detail"),

    path('student-detailed-info/', views.StudentDetailedInfoListCreateAPIView.as_view(),
         name='student-detailed-info-list'),
    path('student-detailed-info/<int:id>/', views.StudentDetailedInfoRetrieveUpdateAPIView.as_view(),
         name='student-detailed-info-detail'),
    path('user-student-detailed-info/<int:user_id>/', views.UserStudentDetailedInfoRetrieveAPIView.as_view(),
         name='user-student-detailed-info-detail'),

    path('basic-form-fields/', views.BasicFormFieldListAPIView.as_view(),
         name="basic-form-fields-list"),

    # path('gmat-certificates/', views.GMATCertificateListCreateAPIView.as_view(),
    #      name="gmat-certificate-list"),
    # path('gmat-certificates/<int:id>/', views.GMATCertificateRetrieveDestroyAPIView.as_view(),
    #      name="gmat-certificate-detail"),
    #
    # path('gre-certificates/', views.GRECertificateListCreateAPIView.as_view(),
    #      name="gre-certificate-list"),
    # path('gre-certificates/<int:id>/', views.GRECertificateRetrieveDestroyAPIView.as_view(),
    #      name="gre-certificates-detail"),

    path('publications/', views.PublicationListCreateAPIView.as_view(),
         name="publication-list"),
    path('publications/<int:id>/', views.PublicationRetrieveDestroyAPIView.as_view(),
         name="publication-detail"),

    path('want-to-applies/', views.WantToApplyListCreateAPIView.as_view(),
         name="want-to-apply-list"),
    path('want-to-applies/<int:id>/', views.WantToApplyRetrieveDestroyAPIView.as_view(),
         name="want-to-apply-detail"),

    path('student-detailed-university-throughs/',
         views.StudentDetailedUniversityThroughListCreateAPIView.as_view(),
         name="student-detailed-university-through-list"),
    path('student-detailed-university-throughs/<int:id>/',
         views.StudentDetailedUniversityThroughRetrieveDestroyAPIView.as_view(),
         name="student-detailed-university-through-detail"),

    # path('student-detailed-language-certificate-type-throughs/',
    #      views.StudentDetailedLanguageCertificateTypeThroughListCreateAPIView.as_view(),
    #      name="student-detailed-language-certificate-type-through-list"),
    # path('student-detailed-language-certificate-type-throughs/<int:id>/',
    #      views.StudentDetailedLanguageCertificateTypeThroughRetrieveDestroyAPIView.as_view(),
    #      name="student-detailed-language-certificate-type-through-detail"),
]


