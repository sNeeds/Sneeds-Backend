"""abroadin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('apis-auth/', include('rest_framework.urls')),

                  path('docs/', include('abroadin.apps.docs.urls')),
                  path('chat/', include('abroadin.apps.chats.urls')),
                  path('utils/', include('abroadin.apps.customUtils.urls')),
                  path('users/', include('abroadin.apps.users.urls')),
                  path('data/', include('abroadin.apps.data.urls')),
                  path('store/', include('abroadin.apps.store.urls')),
                  path('analyze/', include('abroadin.apps.estimation.urls')),
                  path('analytics/', include('abroadin.apps.analytics.urls')),
                  path('apply-profile/', include('abroadin.apps.applyprofile.urls')),
                  path('test/', include('abroadin.apps.testapps.urls')),
                  path('__debug__/', include(debug_toolbar.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
