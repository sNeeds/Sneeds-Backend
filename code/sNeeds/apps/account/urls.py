from django.urls import path

import sNeeds.apps.consultants.views
from . import views

app_name = "account"


urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<str:slug>/', views.CountryDetail.as_view(), name="country-detail"),

    path('universities/', views.UniversityList.as_view(), name="university-list"),
    path('universities/<int:id>/', views.UniversityDetail.as_view(), name="university-detail"),
    path('form-universities/', views.UniversityForFormList.as_view(), name='form-university-list'),

    path('field-of-studies/', views.FieldOfStudyList.as_view(), name="field-of-study-list"),
    path('field-of-studies/<int:id>/', views.FieldOfStudyDetail.as_view(), name="field-of-study-detail"),
    path('form-field-of-studies/', views.FieldOfStudyForFormList.as_view(), name='form-field-of-study-list'),

    path('consultant-profiles/', sNeeds.apps.consultants.views.ConsultantProfileList.as_view(),
         name="consultant-profile-list"),
    path('consultant-profiles/<str:slug>/', sNeeds.apps.consultants.views.ConsultantProfileDetail.as_view(),
         name="consultant-profile-detail"),

    path('student-detailed-info/', views.StudentDetailedInfoListCreateAPIView.as_view(),
         name='student-detailed-info-list'),
    path('student-detailed-info/<uuid:id>/', views.StudentDetailedInfoRetrieveUpdateAPIView.as_view(),
         name='student-detailed-info-detail'),
    path('user-student-detailed-info/<int:user_id>/', views.UserStudentDetailedInfoRetrieveAPIView.as_view(),
         name='user-student-detailed-info-detail'),

    path('basic-form-fields/', views.BasicFormFieldListAPIView.as_view(),
         name="basic-form-fields-list"),

    path('regular-certificates/', views.RegularLanguageCertificateListCreateAPIView.as_view(),
         name="regular-certificate-list"),
    path('regular-certificates/<int:id>/', views.RegularLanguageCertificateRetrieveDestroyAPIView.as_view(),
         name="regular-certificate-detail"),

    path('gmat-certificates/', views.GMATCertificateListCreateAPIView.as_view(),
         name="gmat-certificate-list"),
    path('gmat-certificates/<int:id>/', views.GMATCertificateRetrieveDestroyAPIView.as_view(),
         name="gmat-certificate-detail"),

    path('gre-general-certificates/', views.GREGeneralCertificateListCreateAPIView.as_view(),
         name="gre-general-certificate-list"),
    path('gre-general-certificates/<int:id>/', views.GREGeneralCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-general-certificate-detail"),

    path('gre-subject-certificates/', views.GRESubjectCertificateListCreateAPIView.as_view(),
         name="gre-subject-certificate-list"),
    path('gre-subject-certificates/<int:id>/', views.GRESubjectCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-subject-certificate-detail"),

    path('gre-biology-certificates/', views.GREBiologyCertificateListCreateAPIView.as_view(),
         name="gre-biology-certificate-list"),
    path('gre-biology-certificates/<int:id>/', views.GREBiologyCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-biology-certificate-detail"),

    path('gre-physics-certificates/', views.GREPhysicsCertificateListCreateAPIView.as_view(),
         name="gre-physics-certificate-list"),
    path('gre-physics-certificates/<int:id>/', views.GREPhysicsCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-physics-certificate-detail"),

    path('gre-psychology-certificates/', views.GREPsychologyCertificateListCreateAPIView.as_view(),
         name="gre-psychology-certificate-list"),
    path('gre-psychology-certificates/<int:id>/', views.GREPsychologyCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-psychology-certificate-detail"),

    path('duolingo-certificates/', views.DuolingoCertificateListCreateAPIView.as_view(),
         name="duolingo-certificate-list"),
    path('duolingo-certificates/<int:id>/', views.DuolingoCertificateRetrieveDestroyAPIView.as_view(),
         name="duolingo-certificate-detail"),

    path('publications/', views.PublicationListCreateAPIView.as_view(),
         name="publication-list"),
    path('publications/<int:id>/', views.PublicationRetrieveDestroyAPIView.as_view(),
         name="publication-detail"),

    path('want-to-applies/', views.WantToApplyListCreateAPIView.as_view(),
         name="want-to-apply-list"),
    path('want-to-applies/<int:id>/', views.WantToApplyRetrieveDestroyAPIView.as_view(),
         name="want-to-apply-detail"),

    path('apply-semester-years/', views.StudentFormApplySemesterYearListAPIView.as_view(),
         name="apply-semester-year-list"),
    path('apply-semester-years/<int:id>', views.StudentFormApplySemesterYearRetrieveAPIView.as_view(),
         name="apply-semester-year-detail"),

    path('student-detailed-university-throughs/',
         views.StudentDetailedUniversityThroughListCreateAPIView.as_view(),
         name="student-detailed-university-through-list"),
    path('student-detailed-university-throughs/<int:id>/',
         views.StudentDetailedUniversityThroughRetrieveDestroyAPIView.as_view(),
         name="student-detailed-university-through-detail"),

    path('payment-affordability-choices/',
         views.payment_affordability_choices,
         name="payment-affordability-choice-list"),

    path('grades/', views.GradeChoiceList.as_view(), name="grade-list"),
]


