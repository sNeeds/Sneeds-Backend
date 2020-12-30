from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..base import CartBaseTests

User = get_user_model()


class CartModelTest(CartBaseTests):
    def setUp(self):
        super().setUp()

    def test_price(self):
        self.assertEqual(self.a_cart1.subtotal, 30)

    def test_price_products_add(self):
        self.a_cart1.products.add(self.a_product_3)
        self.assertEqual(self.a_cart1.subtotal, 60)

    def test_price_products_remove(self):
        self.a_cart1.products.remove(self.a_product_2)
        self.assertEqual(self.a_cart1.subtotal, 10)

        self.a_cart1.products.remove(self.a_product_1)
        self.assertEqual(self.a_cart1.subtotal, 0)

    def test_price_products_update(self):
        self.a_product_1.price = 20
        self.a_product_1.save()
        self.a_cart1.refresh_from_db()
        self.assertEqual(self.a_cart1.subtotal, 40)

    def test_price_products_delete(self):
        self.a_product_2.delete()
        self.a_cart1.refresh_from_db()
        self.assertEqual(self.a_cart1.subtotal, 10)

    def test_products_deactived(self):
        self.assertEqual(self.a_cart1.subtotal, 30)
        self.assertEqual(self.a_cart1.products.count(), 2)

        self.a_product_2.active = False
        self.a_product_2.save()
        self.a_cart1.refresh_from_db()
        self.assertEqual(self.a_cart1.products.count(), 1)
        self.assertEqual(self.a_cart1.subtotal, 10)

    def test_products_add_deactive(self):
        self.a_product_1.active = False
        self.a_product_1.save()
        self.assertRaises(ValidationError, self.a_cart1.products.add, self.a_product_1)
