from django.urls import include, path

urlpatterns = [
                  path('packages/', include('abroadin.apps.store.storePackages.urls')),
                  path('base/', include('abroadin.apps.store.storeBase.urls')),
                  path('cart/', include('abroadin.apps.store.carts.urls')),
                  path('order/', include('abroadin.apps.store.orders.urls')),
                  path('payment/', include('abroadin.apps.store.payments.urls')),
                  path('comment/', include('abroadin.apps.store.comments.urls')),
                  path('discount/', include('abroadin.apps.store.discounts.urls')),
                  path('videochat/', include('abroadin.apps.store.videochats.urls')),
                  path('basic-product/', include('abroadin.apps.store.basicProducts.urls')),
]
