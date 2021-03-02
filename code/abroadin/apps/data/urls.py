from django.urls import include, path

urlpatterns = [
                    path('account/', include('abroadin.apps.data.globaldata.urls')),
                    path('apply-data/', include('abroadin.apps.data.applydata.urls')),
]
