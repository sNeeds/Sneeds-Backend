from rest_framework.test import APITestCase

from ..models import Order, ORDER_STATUS_CHOICES
from ...carts.models import Cart
from ...storeBase.models import Product
from ...tests.base import StoreBaseTest
from ...carts.tests.base import CartBaseTests


class OrderTestBase(StoreBaseTest):

    def setUp(self):
        StoreBaseTest.setUp(self)
        self.a_product_1 = Product.objects.create(price=10, active=True)
        self.a_product_2 = Product.objects.create(price=20, active=True)
        self.a_product_3 = Product.objects.create(price=30, active=True)

        self.a_cart1 = Cart.objects.create(user=self.user1)
        self.a_cart1.products.add(self.a_product_1, self.a_product_2)

        self.a_order_1 = Order.objects.create(
            user=self.user1,
            status=ORDER_STATUS_CHOICES[0][0],
            total=20000,
            subtotal=18000,
        )

        self.a_order_2 = Order.objects.create(
            user=self.user1,
            status=ORDER_STATUS_CHOICES[1][0],
            total=10000,
            subtotal=11000,
        )

        self.b_order_1 = Order.objects.create(
            user=self.user2,
            status=ORDER_STATUS_CHOICES[0][0],
            total=20000,
            subtotal=18000,
        )


