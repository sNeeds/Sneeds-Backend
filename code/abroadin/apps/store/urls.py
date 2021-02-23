from django.urls import include, path

urlpatterns = [
                  path('base/', include('abroadin.apps.store.storeBase.urls')),
                  path('cart/', include('abroadin.apps.store.carts.urls')),
                  path('order/', include('abroadin.apps.store.orders.urls')),
                  path('payment/', include('abroadin.apps.store.payments.urls')),
                  path('apply-profile/', include('abroadin.apps.store.applyprofilestore.urls')),
]
