from django.contrib.auth import get_user_model

from abroadin.base.mixins.tests import TestBriefMethodMixin
from ..base import CartBaseTests

User = get_user_model()


class CartAPIBaseTests(TestBriefMethodMixin, CartBaseTests):
    def setUp(self):
        super().setUp()

    def _test_cart_list(self, *args, **kwargs):
        return self._endpoint_test_method('store.cart:cart-list', *args, **kwargs)

    def _test_cart_detail(self, *args, **kwargs):
        return self._endpoint_test_method('store.cart:cart-detail', *args, **kwargs)

