from django.urls import path

from . import views

app_name = "estimation.form"

urlpatterns = [
    path('student-detailed-info/', views.StudentDetailedInfoListCreateView.as_view(),
         name='student-detailed-info-list'),
    path('student-detailed-info/<int:id>/', views.StudentDetailedInfoRetrieveUpdateView.as_view(),
         name='student-detailed-info-detail'),
]
