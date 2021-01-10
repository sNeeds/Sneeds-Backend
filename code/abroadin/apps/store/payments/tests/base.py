from django.contrib.auth import get_user_model

from abroadin.apps.store.storeBase.models import Product
from abroadin.apps.store.carts.models import Cart
from abroadin.apps.store.tests.base import StoreBaseTest

User = get_user_model()


class PaymentBaseTests(StoreBaseTest):
    def setUp(self):
        super().setUp()

        self.a_product_1 = Product.objects.create(price=0, active=True)
        self.a_product_2 = Product.objects.create(price=10000, active=True)

        self.a_cart1 = Cart.objects.create(user=self.user1)
        self.a_cart1.products.add(self.a_product_1, self.a_product_2)

        self.a_cart2 = Cart.objects.create(user=self.user1)
        self.a_cart2.products.add(self.a_product_1)

        self.a_cart3 = Cart.objects.create(user=self.user1)
