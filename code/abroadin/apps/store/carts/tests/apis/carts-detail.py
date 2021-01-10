from django.contrib.auth import get_user_model
from rest_framework import status

from abroadin.apps.store.storeBase.models import Product
from .base import CartAPIBaseTest
from ...models import Cart

User = get_user_model()


class CartAPICartsDetailTests(CartAPIBaseTest):

    def setUp(self):
        super().setUp()

    def _test_cart_detail(self, *args, **kwargs):
        return self._endpoint_test_method('carts:cart-detail', *args, **kwargs)

    def test_get_200(self):
        def get_cart(user, cart):
            self._test_cart_detail("get", user, status.HTTP_200_OK,
                                   reverse_args=cart.id)

        get_cart(self.user1, self.a_cart1)

    def test_get_401(self):
        def get_cart(user, cart):
            self._test_cart_detail("get", user, status.HTTP_401_UNAUTHORIZED,
                                   reverse_args=cart.id)

        get_cart(None, self.a_cart1)

    def test_get_403(self):
        def get_cart(user, cart):
            self._test_cart_detail("get", user, status.HTTP_403_FORBIDDEN,
                                   reverse_args=cart.id)

        get_cart(self.user2, self.a_cart1)

