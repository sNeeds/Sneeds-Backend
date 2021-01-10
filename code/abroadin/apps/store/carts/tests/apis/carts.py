from django.contrib.auth import get_user_model
from rest_framework import status

from abroadin.apps.store.storeBase.models import Product
from .base import CartAPIBaseTest
from ...models import Cart

User = get_user_model()


class CartAPICartsTests(CartAPIBaseTest):

    def setUp(self):
        super().setUp()

        self.t_product_1_free = Product.objects.create(price=0)

    def _test_cart_list(self, *args, **kwargs):
        return self._endpoint_test_method('carts:cart-list', *args, **kwargs)

    def test_get_200(self):
        def get_carts_list(req_func, user):
            data = req_func("get", user, status.HTTP_200_OK)
            self.assertEqual(len(data), Cart.objects.filter(user=user).count())

        get_carts_list(self._test_cart_list, self.user1)
        get_carts_list(self._test_cart_list, self.user2)

    def test_create_201(self):
        def create_normal_cart(user):
            self._test_cart_list("post", user, status.HTTP_201_CREATED,
                                 data={"products": [self.a_product_1.id, self.a_product_2.id]})

        def create_empty_cart(user):
            self._test_cart_list("post", user, status.HTTP_201_CREATED)

        def create_free_cart(user):
            self._test_cart_list("post", user, status.HTTP_201_CREATED,
                                 data={"products": [self.t_product_1_free.id]})

        create_normal_cart(self.user1)
        create_normal_cart(self.user2)

        create_empty_cart(self.user1)
        create_empty_cart(self.user2)

        create_free_cart(self.user1)
        create_free_cart(self.user2)

    def test_create_401(self):
        def create_cart(user):
            self._test_cart_list("post", user, status.HTTP_401_UNAUTHORIZED,
                                 data={"products": [self.a_product_1.id, self.a_product_2.id]})

        create_cart(None)
