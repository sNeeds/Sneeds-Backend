from django.urls import path, include

from .customAuth.views import SubscribeAPIView

urlpatterns = [
    path('auth/', include('abroadin.apps.users.customAuth.urls')),
    path('auth/social/', include('abroadin.apps.users.socialauth.urls')),
    path('subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
]
