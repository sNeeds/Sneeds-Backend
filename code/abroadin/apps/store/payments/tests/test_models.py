from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from abroadin.apps.store.payments.models import ConsultantDepositInfo
from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class ConsultantDepositInfoAPITests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.client = APIClient()

    def test_consultant_deposit_info_create_correct(self):
        consultant_deposit_info_1 = ConsultantDepositInfo.objects.create(consultant=self.consultant1_profile,
                                                                         amount=400)
        self.assertIsNotNone(consultant_deposit_info_1.consultant_deposit_info_id)
        self.assertEqual(consultant_deposit_info_1.amount, 400)
