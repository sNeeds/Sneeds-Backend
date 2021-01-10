from django.contrib.auth import get_user_model

from abroadin.base.mixins.tests import TestBriefMethodMixin
from ..base import CartBaseTests

User = get_user_model()


class CartAPIBaseTest(CartBaseTests, TestBriefMethodMixin):
    def setUp(self):
        super().setUp()
