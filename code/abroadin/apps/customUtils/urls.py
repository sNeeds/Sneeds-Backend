from django.urls import path

from . import views

app_name = "customUtils"

urlpatterns = [
    path('timezone-time/<str:timezone>/', views.TimezoneTimeDetailAPIView.as_view()),
]
