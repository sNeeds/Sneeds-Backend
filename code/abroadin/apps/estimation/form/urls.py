from django.urls import path

from . import views

app_name = "estimation.form"

urlpatterns = [
    path('student-detailed-infos/', views.StudentDetailedInfoListCreateView.as_view(),
         name='student-detailed-info-list'),

    path('student-detailed-infos/<int:id>/', views.StudentDetailedInfoRetrieveUpdateView.as_view(),
         name='student-detailed-info-detail'),

    path('user-student-detailed-info/<int:user_id>/', views.UserStudentDetailedInfoRetrieveAPIView.as_view(),
         name='user-student-detailed-info-detail'),
]
