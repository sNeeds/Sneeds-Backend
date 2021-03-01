from django.urls import path, include

from . import views

app_name = "socialauth"

urlpatterns = [
    path('google/', views.GoogleSocialAuthView.as_view(), name='google-login'),
    path('facebook/', views.FacebookSocialAuthView.as_view(), name='facebook-login'),
]
