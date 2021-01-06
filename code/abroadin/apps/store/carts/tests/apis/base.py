from django.contrib.auth import get_user_model

from abroadin.base.mixins.tests import TestBriefMethodMixin
from ..base import CartBaseTests

User = get_user_model()


class CartAPIBaseTest(CartBaseTests, TestBriefMethodMixin):
    def setUp(self):
        super().setUp()


    def _test_cart_detail(self, *args, **kwargs):
        return self._endpoint_test_method('carts:cart-detail', *args, **kwargs)
