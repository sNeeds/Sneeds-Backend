from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from abroadin.apps.store.storeBase.models import SoldTimeSlotSale

from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class ConsultantTests(CustomAPITestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()

        self.sold_time_slot_sale1 = SoldTimeSlotSale.objects.create(
            sold_to=self.user1,
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            price=self.consultant1_profile.time_slot_price
        )

        self.sold_time_slot_sale2 = SoldTimeSlotSale.objects.create(
            sold_to=self.user2,
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=2),
            price=self.consultant1_profile.time_slot_price
        )

        self.sold_time_slot_sale3 = SoldTimeSlotSale.objects.create(
            sold_to=self.user2,
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            price=self.consultant2_profile.time_slot_price
        )

        # Setup ------
        self.client = APIClient()

    def test_consultant_profile_model_rate_correct(self):
        self.consultant1_profile.refresh_from_db()
        self.assertEqual(self.consultant1_profile.rate, 3.25)

        self.consultant2_profile.refresh_from_db()
        self.assertEqual(self.consultant2_profile.rate, None)
