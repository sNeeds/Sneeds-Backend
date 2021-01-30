from django.urls import path

from . import views

app_name = "data.applydata"

urlpatterns = [
    path('choices/grades/', views.GradesListView.as_view()),

    path('choices/apply-semester-years/', views.SemesterYearListView.as_view(),
         name="apply-semester-year-list"),

    path('choices/language-certificate/', views.LanguageCertificateTypeListView.as_view(),
         name="language-certificate-choices-list"),

    path('choices/which-author/', views.WhichAuthorChoicesListView.as_view(),
         name="which-author-choices-list"),

    path('choices/publication/', views.PublicationChoicesListView.as_view(),
         name="publication-choices-list"),

    path('choices/journal-reputation/', views.JournalReputationChoicesListView.as_view(),
         name="journal-reputation-choices-list"),
]
