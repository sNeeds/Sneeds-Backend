from django.urls import path

from . import views

app_name = "estimations"

urlpatterns = [
    path('import-top-universities/', views.ListUsers.as_view(),),
]
