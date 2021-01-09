from django.contrib.auth import get_user_model

from abroadin.base.mixins.tests import TestBriefMethodMixin
from ..base import PaymentBaseTests

User = get_user_model()


class PaymentAPIBaseTest(PaymentBaseTests, TestBriefMethodMixin):
    def setUp(self):
        super().setUp()
