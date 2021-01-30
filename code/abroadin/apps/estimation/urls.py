from django.urls import include, path

urlpatterns = [
                  path('form/', include('abroadin.apps.estimation.form.urls')),
                  path('estimation/', include('abroadin.apps.estimation.estimations.urls')),
                  path('charts/', include('abroadin.apps.estimation.analyze.urls')),
                  path('similar-profiles/', include('abroadin.apps.estimation.similarprofiles.urls')),
]
