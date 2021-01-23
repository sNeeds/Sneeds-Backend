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
]
