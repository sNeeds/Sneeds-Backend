from django.contrib.auth import get_user_model
from rest_framework import status

from abroadin.apps.store.storeBase.models import Product
from .base import PaymentAPIBaseTest

User = get_user_model()


class PaymentAPIRequestTests(PaymentAPIBaseTest):
    def setUp(self):
        super().setUp()

    def _test_request(self, *args, **kwargs):
        return self._endpoint_test_method('payment:request', *args, **kwargs)

    def create_payment(self, user, cart, status):
        data = self._test_request("post", user, status.HTTP_201_CREATED, data={"cartid": cart.id})
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

        data = self.create_payment(self.user1, self.a_cart3, status.HTTP_400_BAD_REQUEST)
        check_empty_cart_response(data)

        data = self.create_payment(self.user1, self.a_cart2, status.HTTP_400_BAD_REQUEST)
        check_zarinpal_error(data)
