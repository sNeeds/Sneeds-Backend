from zeep import Client

from django.conf import settings

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from abroadin.settings.config.variables import FRONTEND_URL
from abroadin.base.api.permissions import permission_class_factory
from abroadin.base.api.viewsets import CAPIView
from abroadin.apps.store.orders.models import Order
from abroadin.apps.store.carts.models import Cart

from .serializers import PaymentVerifySerializer
from .models import PayPayment
from .permissions import CartOwnerPermission, PayPaymentOwnerPermission

ZARINPAL_MERCHANT = settings.ZARINPAL_MERCHANT


class ZeroPriceHasProductException(Exception):
    pass


class CartEmptyException(Exception):
    pass


class SendRequest(CAPIView):
    """
    POST:
    {
        "cartid":12
    }
    """
    permission_classes = [
        permissions.IsAuthenticated,
        permission_class_factory(CartOwnerPermission, apply_on=['POST'])
    ]

    def _post_pay_request(self, client, cart):
        result = client.service.PaymentRequest(
            ZARINPAL_MERCHANT,
            int(cart.total),
            "پرداخت ابرادین",
            cart.user.email,
            cart.user.phone_number,
            FRONTEND_URL + "user/payment/accept/",
        )
        return result

    def get_user(self):
        return self.request.user

    def _get_cart_or_raise_exception(self, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            raise NotFound(detail={"detail": "Cart does not exist"})
        return cart

    def get_cart_or_none(self):
        data = self.request.data
        cart_id = data.get('cartid')

        if cart_id:
            cart = self._get_cart_or_raise_exception(cart_id)
            return cart

        return None

    def check_result_ok(self, result):
        return result.Status == 100

    def create_payment_object(self, user, cart, authority):
        PayPayment.objects.create(user=user, cart=cart, authority=authority)

    def send_pay_request(self, client, cart):
        is_zero_price_acceptable = cart.is_total_zero() and cart.has_product()

        if not cart.has_product():
            raise CartEmptyException
        elif is_zero_price_acceptable:
            raise ZeroPriceHasProductException

        result = self._post_pay_request(client, cart)

        return result

    def sell_cart(self, cart):
        return Order.objects.sell_cart_create_order(cart)

    def is_user_cart_owner_permission(self, user, cart):
        return cart.user == user

    def zero_price_has_product_response(self, order_id):
        return Response({"detail": "Success", "ReflD": "00000000", "order": order_id}, 201)

    def cart_empty_response(self):
        return Response({"detail": "Cart is empty"}, 400)

    def payment_request_ok_response(self, result):
        return Response({"redirect": 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)}, 201)

    def payment_request_not_ok_response(self, result):
        return Response({"detail": 'Zarinpal error', 'code': str(result.Status)}, 400)

    def post(self, request, *args, **kwargs):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

        user = self.get_user()
        cart = self.get_cart_or_none()

        try:
            result = self.send_pay_request(client, cart)
            result_ok = self.check_result_ok(result)
            if result_ok:
                self.create_payment_object(user, cart, result.Authority)
                response = self.payment_request_ok_response(result)
            else:
                response = self.payment_request_not_ok_response(result)
        except ZeroPriceHasProductException:
            order = self.sell_cart(cart)
            response = self.zero_price_has_product_response(order_id=order.id)
        except CartEmptyException:
            response = self.cart_empty_response()
        except Exception as e:
            raise e

        return response


class Verify(CAPIView):
    """
    POST:
    {
       "authority":"000000000000000000000000000150139347",
       "status":"OK"
    }

    """
    permission_classes = [
        permissions.IsAuthenticated,
        permission_class_factory(PayPaymentOwnerPermission, apply_on=['POST'])
    ]

    def get_data(self):
        return self.request.data

    def get_user(self):
        return self.request.user

    def get_payment(self, authority):
        try:
            payment = PayPayment.objects.get(authority=authority)
        except PayPayment.DoesNotExist:
            raise NotFound({"detail": "No paypayment with this user and authority exists"})
        return payment

    def get_payment_or_none(self):
        data = self.get_data()
        authority = data.get('authority')

        if authority:
            payment = self.get_payment(authority)
            return payment

        return None

    def is_status_ok(self, status):
        return status == 'OK'

    def sell_cart(self, cart):
        return Order.objects.sell_cart_create_order(cart)

    def transaction_ok_handler(self, client, authority):
        payment = self.get_payment(authority)

        total = int(payment.cart.total)
        result = client.service.PaymentVerification(ZARINPAL_MERCHANT, authority, total)

        if result.Status == 100:
            order = self.sell_cart(payment.cart)
            response = self.order_created_response(result.RefID, order)
        else:
            response = self.transaction_verification_failed_response(result.Status)

        return response

    def post(self, request):
        data = self.get_data()
        serializer = PaymentVerifySerializer(data=data)

        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data["status"]
        authority = serializer.validated_data["authority"]

        status_ok = self.is_status_ok(status)
        if status_ok:
            client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
            response = self.transaction_ok_handler(client, authority)
        else:
            response = self.transaction_nok_response()

        return response

    def order_created_response(self, ref_id, order):
        return Response({"detail": "Success", "ReflD": str(ref_id), "order": order.id}, status=200)

    def transaction_verification_failed_response(self, status):
        return Response({"detail": "Transaction verification failed", "status": str(status)}, status=400)

    def transaction_nok_response(self):
        return Response({"detail": "Transaction failed or canceled by user"}, status=400)
