from rest_framework.exceptions import APIException
from zeep import Client

from django.conf import settings

from rest_framework import permissions
from rest_framework.response import Response

from abroadin.base.api import generics
from abroadin.apps.store.orders.models import Order
from abroadin.base.api.generics import CListAPIView
from abroadin.base.api.viewsets import CAPIView
from .serializers import ConsultantDepositInfoSerializer
from .permissions import ConsultantDepositInfoOwner
from .models import ConsultantDepositInfo
from abroadin.apps.users.consultants.models import ConsultantProfile
from .models import PayPayment
from abroadin.apps.store.carts.models import Cart
from abroadin.settings.config.variables import FRONTEND_URL
from abroadin.utils.custom.custom_permissions import IsConsultantPermission

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
    permission_classes = [permissions.IsAuthenticated, ]

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

    def get_user(self, request):
        return request.user

    def get_cart(self, cart_id):
        cart = Cart.objects.get(id=cart_id)
        return cart

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

    def zero_price_has_product_response(self, order_id):
        return Response({"detail": "Success", "ReflD": "00000000", "order": order_id}, 201)

    def cart_empty_response(self):
        return Response({"detail": "Cart is empty."}, 400)

    def payment_request_ok_response(self, result):
        return Response({"redirect": 'https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority)}, 201)

    def payment_request_not_ok_response(self, result):
        return Response({"detail": 'Error code: ' + str(result.Status)}, 400)

    def post(self, request, *args, **kwargs):
        data = request.data
        client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')

        user = self.get_user(request)
        cart = self.get_cart(data.get('cartid'))

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
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')

        data = request.data
        if data.get('status') == 'OK':
            user = request.user
            authority = data.get('authority', None)

            try:
                payment = PayPayment.objects.get(
                    user=user,
                    authority=authority
                )

            except PayPayment.DoesNotExist:
                return Response({"detail": "PayPayment does not exists."}, status=400)

            result = client.service.PaymentVerification(ZARINPAL_MERCHANT, authority, int(payment.cart.total))

            if result.Status == 100:
                order = Order.objects.sell_cart_create_order(payment.cart)
                # TODO RefID does not save in relative order or in payment ???
                return Response(
                    {"detail": "Success",
                     "ReflD": str(result.RefID),
                     "order": order.id},
                    status=200
                )
            elif result.Status == 101:
                return Response({"detail": "Transaction submitted", "status": str(result.Status)}, status=200)
            else:
                return Response({"detail": "Transaction failed", "status": str(result.Status)}, status=400)

        else:
            return Response({"detail": "Transaction failed or canceled by user"}, status=400)


