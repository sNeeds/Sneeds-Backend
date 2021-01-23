from django.urls import path

from . import views

app_name = "estimation.form"

urlpatterns = [
    path('student-detailed-info/', views.StudentDetailedInfoListCreateAPIView.as_view(),
         name='student-detailed-info-list'),
    path('student-detailed-info/<int:id>/', views.StudentDetailedInfoRetrieveUpdateAPIView.as_view(),
         name='student-detailed-info-detail'),
    path('user-student-detailed-info/<int:user_id>/', views.UserStudentDetailedInfoRetrieveAPIView.as_view(),
         name='user-student-detailed-info-detail'),

    path('basic-form-fields/', views.BasicFormFieldListAPIView.as_view(),
         name="basic-form-fields-list"),

    path('certificates/regular/', views.RegularLanguageCertificateListCreateAPIView.as_view(),
         name="regular-list"),
    path('certificates/regular/<int:id>/', views.RegularLanguageCertificateRetrieveDestroyAPIView.as_view(),
         name="regular-detail"),

    path('certificates/gmat/', views.GMATCertificateListCreateAPIView.as_view(),
         name="gmat-list"),
    path('certificates/gmat/<int:id>/', views.GMATCertificateRetrieveDestroyAPIView.as_view(),
         name="gmat-detail"),

    path('certificates/gre-general/', views.GREGeneralCertificateListCreateAPIView.as_view(),
         name="gre-general-list"),
    path('certificates/gre-general/<int:id>/', views.GREGeneralCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-general-detail"),

    path('certificates/gre-subject/', views.GRESubjectCertificateListCreateAPIView.as_view(),
         name="gre-subject-list"),
    path('certificates/gre-subject/<int:id>/', views.GRESubjectCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-subject-detail"),

    path('certificates/gre-biology/', views.GREBiologyCertificateListCreateAPIView.as_view(),
         name="gre-biology-list"),
    path('certificates/gre-biology/<int:id>/', views.GREBiologyCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-biology-detail"),

    path('certificates/gre-physics/', views.GREPhysicsCertificateListCreateAPIView.as_view(),
         name="gre-physics-list"),
    path('certificates/gre-physics/<int:id>/', views.GREPhysicsCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-physics-detail"),

    path('certificates/gre-psychology/', views.GREPsychologyCertificateListCreateAPIView.as_view(),
         name="gre-psychology-list"),
    path('certificates/gre-psychology/<int:id>/', views.GREPsychologyCertificateRetrieveDestroyAPIView.as_view(),
         name="gre-psychology-detail"),

    path('certificates/duolingo/', views.DuolingoCertificateListCreateAPIView.as_view(),
         name="duolingo-list"),
    path('certificates/duolingo/<int:id>/', views.DuolingoCertificateRetrieveDestroyAPIView.as_view(),
         name="duolingo-detail"),

    path('choices/grades/', views.GradesListAPIView.as_view()),

    path('choices/apply-semester-years/', views.SemesterYearListAPIView.as_view(),
         name="apply-semester-year-choices-list"),

    path('choices/gender/', views.GenderChoicesListAPIView.as_view(), name="gender-choices-list"),

    path('choices/which-author/', views.WhichAuthorChoicesListAPIView.as_view(),
         name="which-author-choices-list"),

    path('choices/publication/', views.PublicationChoicesListAPIView.as_view(),
         name="publication-choices-list"),

    path('choices/journal-reputation/', views.JournalReputationChoicesListAPIView.as_view(),
         name="journal-reputation-choices-list"),

    path('choices/payment-affordability/', views.PaymentAffordabilityChoicesListAPIView.as_view(),
         name="payment-affordability-choices-list"),

    path('choices/language-certificate/', views.LanguageCertificateTypeListAPIView.as_view(),
         name="language-certificate-choices-list"),

]
