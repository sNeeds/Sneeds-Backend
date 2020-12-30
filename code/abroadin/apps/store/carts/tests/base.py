from django.contrib.auth import get_user_model

from ..models import Cart
from ...storeBase.models import Product
from ...tests.base import StoreBaseTest

User = get_user_model()


class CartBaseTests(StoreBaseTest):
    def setUp(self):
        super().setUp()

        self.a_product_1 = Product.objects.create(price=10, active=True)
        self.a_product_2 = Product.objects.create(price=20, active=True)
        self.a_product_3 = Product.objects.create(price=30, active=True)

        self.a_cart1 = Cart.objects.create(user=self.user1)
        self.a_cart1.products.add(self.a_product_1, self.a_product_2)