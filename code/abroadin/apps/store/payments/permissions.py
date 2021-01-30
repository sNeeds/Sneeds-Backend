from rest_framework.permissions import BasePermission


class CartOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        user = view.get_user()
        cart = view.get_cart_or_none()

        if cart:
            return cart.user == user

        # For DRF browsable API because requests to endpoint without data
        return True


class PayPaymentOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        user = view.get_user()
        payment = view.get_payment_or_none()

        if payment:
            return payment.user == user

        # For DRF browsable API because requests to endpoint without data
        return True
