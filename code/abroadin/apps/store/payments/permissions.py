from rest_framework.permissions import BasePermission


class CartOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        user = view.get_user()
        cart = view.get_cart_or_none()

        if cart:
            return cart.user == user

        # For DRF view because requests to endpoint without data
        return True
