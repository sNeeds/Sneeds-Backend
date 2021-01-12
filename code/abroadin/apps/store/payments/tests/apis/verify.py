from django.contrib.auth import get_user_model
from rest_framework import status

from .base import PaymentAPIBaseTest
from abroadin.apps.store.payments.models import PayPayment

User = get_user_model()


class PaymentAPIRequestTests(PaymentAPIBaseTest):
    def setUp(self):
        self.wrong_authority = "000000000000000000000000000000295398"

        super().setUp()

    def _test_verify(self, *args, **kwargs):
        return self._endpoint_test_method('payment:verify', *args, **kwargs)

    def post_verify(self, user, authority, payment_status, status):
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
            self.assertEqual(data.get("detail"), "Transaction failed or canceled by user")

        def post_transaction_verification_failed(user):
            data = self._test_verify(
                "post", user, status=status.HTTP_400_BAD_REQUEST,
                data={"statius": "OK", "authority": self.wrong_authority})
            return data

        def check_transaction_verification__failed_response(data):
            self.assertEqual(data.get("detail"), "Transaction verification failed")
            self.assertNotEqual(data.get("status"), None)

        def create_pay_payment_obj(user, cart, authority):
            obj = PayPayment.objects.create(user=user, cart=cart, authority=authority)
            return obj

        data = empty_json_body_request(self.user1)
        check_empty_post_body_response(data)

        data = post_status_nok(self.user1)
        check_nok_response(data)

        paypayment = create_pay_payment_obj(self.user1, self.a_cart1, self.wrong_authority)
        data = post_transaction_verification_failed(self.user1)
        check_transaction_verification__failed_response(data)
        paypayment.delete()

    def test_create_401(self):
        self.post_verify(
            None, self.wrong_authority, "OK", status.HTTP_401_UNAUTHORIZED
        )

    # def test_create_403(self):
    #     self.create_payment(self.user2, self.a_cart1, status.HTTP_403_FORBIDDEN)

    def test_create_404(self):
        def post_no_paypayment_exist(user):
            data = self._test_verify(
                "post", user, status=status.HTTP_400_BAD_REQUEST,
                data={"detail":})
            return data

        def check_post_no_paypayment_exist_response(data):
            self.assertEqual(data.get("detail"), "No paypayment with this user and authority exists")

        data = post_no_paypayment_exist(self.user1)
        check_post_no_paypayment_exist_response(data)
