from django.urls import path

from . import views

app_name = "estimations"

urlpatterns = [
    path('form-comments/<int:id>/', views.FormComments.as_view()),

    path('import-top-universities/', views.ListUsers.as_view(), ),
]
