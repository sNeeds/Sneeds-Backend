from django.urls import include, path

urlpatterns = [
                  path('events/', include('abroadin.apps.analytics.events.urls')),
]
