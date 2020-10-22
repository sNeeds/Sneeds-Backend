from django.urls import path

from . import views

url_patterns = [
    path('generate-verification/', views.GenerateVerificationAPIView.as_view(), name='generate-verification'),
    path('verify-verification/', views.VerifyVerificationAPIView.as_view(), name='verify-verification'),
]
