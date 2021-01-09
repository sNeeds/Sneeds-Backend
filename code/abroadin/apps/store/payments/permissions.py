from rest_framework.permissions import BasePermission


class CartOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        user = view.get_user()
        cart = view.get_cart()

        return cart.user == user
