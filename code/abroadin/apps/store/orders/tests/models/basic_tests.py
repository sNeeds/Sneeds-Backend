from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.store.applyprofilestore.models import ApplyProfileGroup
from abroadin.apps.store.carts.models import Cart
from ...models import Order
from .base import OrderModelsTestBase


class OrderBasicModelTests(OrderModelsTestBase):
    def setUp(self):
        super().setUp()

    def test_sell_cart(self):
        app_profile_group1 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )
        app_profile_group2 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )

        applyprofile1 = ApplyProfile.objects.create(
            name='applyprofile1',
            gap=10,
        )

        applyprofile2 = ApplyProfile.objects.create(
            name='applyprofile2',
            gap=10,
        )

        app_profile_group1.apply_profiles.set([applyprofile1, applyprofile2])
        app_profile_group2.apply_profiles.set([applyprofile2])
        cart = Cart.objects.create(user=self.user1)
        cart.products.add(app_profile_group1, app_profile_group2)

        order = Order.objects.sell_cart_create_order(cart)
        self.assertEqual(order.status, 'paid')
        self.assertEqual(order.total, cart.total)
        self.assertEqual(order.subtotal, cart.subtotal)
        self.assertEqual(order.sold_products.all().count(), 2)
        self.assertEqual(order.user.id, cart.user.id)

    def test_order_id_creation(self):
        order = Order.objects.create(
            user=self.user1,
            total=50000,
            subtotal=40000,
        )

        self.assertIsNotNone(order.order_id)