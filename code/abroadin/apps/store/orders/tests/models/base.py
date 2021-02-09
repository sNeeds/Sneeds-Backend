from abroadin.apps.store.storeBase.models import Product
from abroadin.apps.store.carts.models import Cart

from ..base import OrderTestBase
from ...models import Order


class OrderModelsTestBase(OrderTestBase):

    def setUp(self):
        super().setUp()
        self.a_product_1 = Product.objects.create(price=10, active=True)
        self.a_product_2 = Product.objects.create(price=20, active=True)
        self.a_product_3 = Product.objects.create(price=30, active=True)

        self.a_cart1 = Cart.objects.create(user=self.user1)
        self.a_cart1.products.add(self.a_product_1, self.a_product_2)

    def test_sell_cart(self):
        order = Order.objects.sell_cart_create_order(self.a_cart1)
        self.assertEqual(order.status, 'paid')
        self.assertEqual(order.total, self.a_cart1.total)
        self.assertEqual(order.subtotal, self.a_cart1.subtotal)
        # self.assertEqual(order.sold_products.all().count(), 2)
        self.assertEqual(order.user.id, self.a_cart1.user.id)

