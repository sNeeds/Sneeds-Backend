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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),

                  path('docs/', include('abroadin.apps.docs.urls')),
                  path('chat/', include('abroadin.apps.chats.urls')),
                  path('utils/', include('abroadin.apps.customUtils.urls')),
                  path('users/auth/', include('abroadin.apps.users.customAuth.urls')),
                  path('users/consultants/', include('abroadin.apps.users.consultants.urls')),
                  path('users/files/', include('abroadin.apps.users.userFiles.urls')),
                  path('data/account/', include('abroadin.apps.data.account.urls')),
                  path('store/packages/', include('abroadin.apps.store.storePackages.urls')),
                  path('store/base/', include('abroadin.apps.store.storeBase.urls')),
                  path('store/cart/', include('abroadin.apps.store.carts.urls')),
                  path('store/order/', include('abroadin.apps.store.orders.urls')),
                  path('store/payment/', include('abroadin.apps.store.payments.urls')),
                  path('store/comment/', include('abroadin.apps.store.comments.urls')),
                  path('store/discount/', include('abroadin.apps.store.discounts.urls')),
                  path('store/videochat/', include('abroadin.apps.store.videochats.urls')),
                  path('store/basic-product/', include('abroadin.apps.store.basicProducts.urls')),
                  path('analyze/form/', include('abroadin.apps.estimation.form.urls')),
                  path('analyze/estimation/', include('abroadin.apps.estimation.estimations.urls')),
                  path('analyze/similars/', include('abroadin.apps.estimation.similarApply.urls')),
                  path('analyze/charts/', include('abroadin.apps.estimation.analyze.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


