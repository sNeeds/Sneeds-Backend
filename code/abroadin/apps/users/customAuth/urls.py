from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = "auth"

urlpatterns = [
    path('social/', include('allauth.urls')),
    path('jwt/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('accounts/', views.UserListView.as_view()),
    path('accounts/<int:id>/', views.UserDetailView.as_view()),

    path('my-account/', views.MyAccountInfoView.as_view()),

    path('generate-verification/', views.GenerateVerificationAPIView.as_view(), name='generate-verification'),
    path('verify-verification/', views.VerifyVerificationAPIView.as_view(), name='verify-verification'),
]
