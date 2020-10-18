"""sNeeds URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),

                  path('docs/', include('sNeeds.apps.docs.urls')),
                  path('auth/', include('sNeeds.apps.users.customAuth.urls')),
                  path('account/', include('sNeeds.apps.data.account.urls')),
                  path('consultant/', include('sNeeds.apps.users.consultants.urls')),
                  path('store/packages/', include('sNeeds.apps.store.storePackages.urls')),
                  path('store/', include('sNeeds.apps.store.storeBase.urls')),
                  path('cart/', include('sNeeds.apps.store.carts.urls')),
                  path('order/', include('sNeeds.apps.store.orders.urls')),
                  path('payment/', include('sNeeds.apps.store.payments.urls')),
                  path('comment/', include('sNeeds.apps.store.comments.urls')),
                  path('user-file/', include('sNeeds.apps.users.userFiles.urls')),
                  path('discount/', include('sNeeds.apps.store.discounts.urls')),
                  path('videochat/', include('sNeeds.apps.store.videochats.urls')),
                  path('chat/', include('sNeeds.apps.chats.urls')),
                  path('basic-product/', include('sNeeds.apps.store.basicProducts.urls')),
                  path('utils/', include('sNeeds.apps.customUtils.urls')),
                  path('estimation/', include('sNeeds.apps.estimation.estimations.urls')),
                  path('similar-applies/', include('sNeeds.apps.estimation.similarApply.urls')),
                  path('form-charts/', include('sNeeds.apps.estimation.analyze.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

