from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from abroadin.apps.users.consultants.models import ConsultantProfile
from abroadin.base.models.abstracts import InheritanceCastModel

User = get_user_model()


class ProductManager(models.QuerySet):
    def get_time_slot_sales(self):
        pass

    def get_basic_products(self):
        pass

    def get_webinar_products(self):
        pass

    def get_class_products(self):
        pass

    def get_store_packages(self):
        pass

    def get_sold_store_unpaid_package_phases(self):
        pass

    def are_all_active(self):
        return not self.filter(active=False).exists()

    def cast_subclasses(self):
        objs_chain = []
        for obj in self.all():
            objs_chain = chain(objs_chain, [obj.cast()])
        return objs_chain


class SoldProductQuerySet(models.QuerySet):
    pass


class Product(InheritanceCastModel):
    price = models.PositiveIntegerField(blank=True)
    active = models.BooleanField(default=True)

    objects = ProductManager.as_manager()

    @property
    def title(self):
        raise NotImplementedError

    @property
    def subtitle(self):
        raise NotImplementedError

    def sell(self):
        raise NotImplementedError


class SoldProduct(InheritanceCastModel):
    price = models.PositiveIntegerField()
    sold_to = models.ForeignKey(User, blank=True, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = SoldProductQuerySet.as_manager()


