from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.db.models import Sum

from abroadin.apps.store.storeBase.models import Product

User = get_user_model()


class CartManager(models.QuerySet):
    def remove_product(self, product):
        qs = self._chain()
        for obj in qs:
            obj.products.remove(product)
        return qs

    @transaction.atomic
    def new_cart_with_products(self, products, **kwargs):
        obj = self.create(**kwargs)
        obj.products.add(*products)
        return obj

    @transaction.atomic
    def update_price(self):
        qs = self._chain()
        for obj in qs:
            obj.update_price()
            obj.save()
        return qs


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="cart")
    products = models.ManyToManyField(Product, blank=True, related_name="carts")

    subtotal = models.IntegerField(default=0, editable=False)
    total = models.IntegerField(default=0, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager.as_manager()

    class Meta:
        ordering = ["-id"]

    def is_total_zero(self):
        return self.total == 0

    def has_product(self):
        return self.products.exists()

    def update_price(self):
        subtotal = self.products.aggregate(subtotal=Sum('price'))['subtotal'] or 0
        self.subtotal = subtotal
        self.total = subtotal

    def update_products(self):
        products_qs = self.products.all()

        for product in products_qs:
            if not product.active:
                self.products.remove(product)

        self.save()

    def sell(self):
        products = self.products.all()
        casted_products = products.cast_subclasses()
        sold_products = []
        for product in casted_products:
            sold_product = product.sell()
            if sold_product:
                sold_products.append(sold_product)
        return sold_products

    def __str__(self):
        return "User {} cart | pk: {}".format(self.user, str(self.pk))
