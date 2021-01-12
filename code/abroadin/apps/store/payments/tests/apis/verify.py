from django.contrib.auth import get_user_model
from rest_framework import status

from abroadin.apps.store.storeBase.models import Product
from abroadin.apps.store.carts.models import Cart
from .base import PaymentAPIBaseTest

User = get_user_model()


class PaymentAPIRequestTests(PaymentAPIBaseTest):
    def setUp(self):
        self.wrong_authority = "000000000000000000000000000000295398"

        super().setUp()

    def _test_verify(self, *args, **kwargs):
        return self._endpoint_test_method('payment:verify', *args, **kwargs)

    def post_verify(self, user, status, authority, payment_status):
        data = self._test_verify("post", user, status, data={"authority": authority, "status": payment_status})
        return data

    def test_create_400(self):
        def empty_json_body_request(user):
            data = self._test_verify("post", user, status.HTTP_400_BAD_REQUEST)
            return data

        def check_empty_post_body_response(data):
            self.assertEqual(data.get("status"), "This field is required.")
            self.assertEqual(data.get("authority"), "This field is required.")

        def post_status_nok(user):
            data = self._test_verify(
                "post", user, status=status.HTTP_400_BAD_REQUEST,
                data={"statius": "NOK", "authority": self.wrong_authority})
            return data

        def check_nok_response(data):
            self.assertEqual(data.get("detail", "Transaction failed or canceled by user"))

        data = empty_json_body_request(self.user1)
        check_empty_post_body_response(data)

        data = post_status_nok(self.user1)
        check_nok_response(data)

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
