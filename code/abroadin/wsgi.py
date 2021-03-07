"""
WSGI config for abroadin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

DEPLOYMENT = int(os.environ.get('DJANGO_DEPLOYMENT', default=0))

if DEPLOYMENT == 0:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abroadin.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abroadin.settings.deployment')

application = get_wsgi_application()


from abroadin.apps.estimation.similarprofiles.tags import SimilarGPA
from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.estimation.form.models import StudentDetailedInfo

s = SimilarGPA()
# q = ApplyProfile.objects.filter(id__in=[500, 501, 502])
q = ApplyProfile.objects.all()
f = StudentDetailedInfo.objects.get(id=497)

l = s.tag_queryset(q, f)
filter_d = {s.annotation_field: True}
l.filter(**filter_d).values_list()
