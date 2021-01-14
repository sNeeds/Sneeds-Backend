from django.urls import include, path

urlpatterns = [
                path('similar-profiles/', include('abroadin.apps.testapps.similarProfiles.urls')),
]
