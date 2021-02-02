from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import Q
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from abroadin.apps.store.carts.models import Cart
from abroadin.apps.store.discounts.models import Discount, CartDiscount, TimeSlotSaleNumberDiscount
from abroadin.apps.store.storeBase.models import SoldProduct
from abroadin.apps.store.storePackages.models import SoldStorePaidPackagePhase

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('paid', 'Paid'),
    ('canceled_not_refunded', 'Canceled but not refunded'),
    ('canceled_refunded', 'Canceled and refunded'),
)


class OrderManager(models.QuerySet):
    @transaction.atomic
    def sell_cart_create_order(self, cart):
        order = Order.objects.create(
            user=cart.user,
            status='paid',
            total=cart.total,
            subtotal=cart.subtotal,
        )

        for product in cart.products.all():
            product = product.cast().cast_subclasses()
            product.sell()

        cart.delete()

        return order

    def get_customs(self):
        # TODO: Temp for Erfan, rm as fas as you can :))

        ids_list = self.values_list('id', flat=True)
        valid_ids = [i for i in ids_list if i % 10 == 0]
        naive_time = datetime(2020, 7, 20, 0, 0)
        aware_time = make_aware(naive_time)
        return self.filter(Q(id__in=valid_ids) | Q(created__lt=aware_time))


class Order(models.Model):
    order_id = models.CharField(unique=True, max_length=12, blank=True,
                                help_text="Leave this field blank, this will populate automatically."
                                )
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    status = models.CharField(max_length=256, default='paid', choices=ORDER_STATUS_CHOICES)
    sold_products = models.ManyToManyField(SoldProduct, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # TODO:Change to code.
    used_discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    time_slot_sales_number_discount = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    objects = OrderManager.as_manager()

    def get_user(self):
        return self.user

    def __str__(self):
        return "Order: {} | pk: {} ".format(str(self.order_id), str(self.pk))
