from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from abroadin.apps.store.storeBase.models import TimeSlotSale
from abroadin.apps.store.storeBase.tasks import delete_time_slots

from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class StoreTests(CustomAPITestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()

        # Setup ------
        self.client = APIClient()

    def test_celery_task_delete_old_time_slot_sales(self):
        ts = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() - timezone.timedelta(minutes=1),
            end_time=timezone.now() + timezone.timedelta(minutes=1),
            price=self.consultant1_profile.time_slot_price
        )
        delete_time_slots()
        self.assertEqual(
            TimeSlotSale.objects.filter(id=ts.id).count(),
            0
        )
