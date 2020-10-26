from django.urls import path

from . import views

app_name = "estimation.form"

urlpatterns = [
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

    path('want-to-applies/', views.WantToApplyListAPIView.as_view(),
         name="want-to-apply-list"),
    path('want-to-applies/<int:id>/', views.WantToApplyDetailAPIView.as_view(),
         name="want-to-apply-detail"),


    path('university-throughs/', views.UniversityThroughListAPIView.as_view(),
         name="university-through-list"),
    path('university-throughs/<int:id>/', views.UniversityThroughDetailAPIView.as_view(),
         name="university-through-detail"),

    path('choices/grades/', views.GradesListAPIView.as_view()),

    path('choices/apply-semester-years/', views.SemesterYearListAPIView.as_view(),
         name="apply-semester-year-list"),


    path('choices/gender-choices/', views.GenderChoicesListAPIView.as_view(), name="gender-choices-list"),

    path('choices/which-author-choices/', views.WhichAuthorChoicesListAPIView.as_view(),
         name="which-author-choices-list"),

    path('choices/publication-choices/', views.PublicationChoicesListAPIView.as_view(),
         name="publication-choices-list"),

    path('choices/journal-reputation-choices/', views.JournalReputationChoicesListAPIView.as_view(),
         name="journal-reputation-choices-list"),

    path('choices/payment-affordability-choices/', views.PaymentAffordabilityChoicesListAPIView.as_view(),
         name="payment-affordability-choices-list"),

    path('choices/language-certificate-choices/', views.LanguageCertificateTypeListAPIView.as_view(),
         name="language-certificate-choices-list"),

]
