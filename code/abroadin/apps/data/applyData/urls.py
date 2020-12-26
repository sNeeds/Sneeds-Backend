from django.urls import path

from . import views

app_name = "data.applyData"

urlpatterns = [
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

    path('choices/grades/', views.GradesListAPIView.as_view()),

    path('choices/apply-semester-years/', views.SemesterYearListAPIView.as_view(),
         name="apply-semester-year-list"),

    path('choices/language-certificate-choices/', views.LanguageCertificateTypeListAPIView.as_view(),
         name="language-certificate-choices-list"),
]
