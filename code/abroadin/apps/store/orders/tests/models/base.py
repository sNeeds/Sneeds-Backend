from abroadin.apps.store.storeBase.models import Product
from abroadin.apps.store.carts.models import Cart

from ..base import OrderTestBase


class OrderModelsTestBase(OrderTestBase):

    def setUp(self):
        super().setUp()
        self.a_product_1 = Product.objects.create(price=10, active=True)
        self.a_product_2 = Product.objects.create(price=20, active=True)
        self.a_product_3 = Product.objects.create(price=30, active=True)

        self.a_cart1 = Cart.objects.create(user=self.user1)
        self.a_cart1.products.add(self.a_product_1, self.a_product_2)
