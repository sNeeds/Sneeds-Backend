from django.contrib.auth import get_user_model

from ..base import CartBaseTests

User = get_user_model()


class CartModelBaseTests(CartBaseTests):
    def setUp(self):
        super().setUp()
