from django.urls import path, include

urlpatterns = [
    path('where-is-better/', include('abroadin.apps.campaigns.wherebetter.urls'))
]
