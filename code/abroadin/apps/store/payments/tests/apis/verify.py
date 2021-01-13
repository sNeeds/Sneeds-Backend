from django.contrib.auth import get_user_model
from rest_framework import status

from abroadin.apps.store.storeBase.models import Product
from abroadin.apps.store.carts.models import Cart
from .base import PaymentAPIBaseTest

User = get_user_model()


class PaymentAPIRequestTests(PaymentAPIBaseTest):
    def setUp(self):
        super().setUp()

    def _test_request(self, *args, **kwargs):
        return self._endpoint_test_method('payment:verify', *args, **kwargs)

    def check_payment(self, user, cart, status):
        data = self._test_request("post", user, status, data={"cartid": cart.id})
        return data

    def test_create_201(self):
        def check_non_zero_price_cart_response(data):
            self.assertNotEqual(data.get("redirect"), None)

        def check_zero_price_cart_response(data):
            self.assertEqual(data.get("detail"), "Success")
            self.assertEqual(data.get("ReflD"), "00000000")
            self.assertNotEqual(data.get("order"), None)

        data = self.create_payment(self.user1, self.a_cart1, status.HTTP_201_CREATED)
        check_non_zero_price_cart_response(data)

        data = self.create_payment(self.user1, self.a_cart2, status.HTTP_201_CREATED)
        check_zero_price_cart_response(data)

    def test_create_400(self):
        def check_empty_cart_response(data):
            self.assertEqual(data.get("detail"), "Cart is empty")

        def check_zarinpal_error(data):
            self.assertEqual(data.get("detail"), "Zarinpal error")
            self.assertNotEqual(data.get("code"), None)

        def create_low_price_cart_for_zarinpal(user):
            """
            Zarinpal rejects under 1000Toman prices
            """
            product = Product.objects.create(price=1)
            cart = Cart.objects.create(user=user)
            cart.products.add(product)
            return cart

        data = self.create_payment(self.user1, self.a_cart3, status.HTTP_400_BAD_REQUEST)
        check_empty_cart_response(data)

        f_cart = create_low_price_cart_for_zarinpal(self.user1)
        data = self.create_payment(self.user1, f_cart, status.HTTP_400_BAD_REQUEST)
        check_zarinpal_error(data)

    def test_create_401(self):
        self.create_payment(None, self.a_cart1, status.HTTP_401_UNAUTHORIZED)

    def test_create_403(self):
        self.create_payment(self.user2, self.a_cart1, status.HTTP_403_FORBIDDEN)

    def test_create_404(self):
        def create_wrong_cart_id(user):
            data = self._test_request("post", user, status.HTTP_404_NOT_FOUND, data={"cartid": -1})
            return data

        def check_wrong_id_response(data):
            self.assertEqual(data.get("detail"), "Cart does not exist")

        data = create_wrong_cart_id(self.user1)
        check_wrong_id_response(data)
