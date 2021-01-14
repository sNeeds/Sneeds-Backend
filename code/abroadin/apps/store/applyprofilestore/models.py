from django.db import models
from django.contrib.contenttypes.models import ContentType

from ..storeBase.models import Product

from abroadin.apps.applyprofile.models import ApplyProfile


class ApplyProfileGroup(Product):
    apply_profiles = models.ManyToManyField(ApplyProfile)

    def title(self):
        return f''

    def subtitle(self):
        return f''


class SoldApplyProfileGroup(Product):
    apply_profiles = models.ManyToManyField(ApplyProfile)

    # def save(self, *args, **kwargs):
    #     self.real_type =


