from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from sNeeds.apps.store.discounts.models import Discount, CartDiscount
from sNeeds.apps.store.storeBase.models import TimeSlotSale
from sNeeds.apps.store.storeBase.tasks import delete_time_slots

from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()



class StoreTests(CustomAPITestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()

        # Consultant discounts
        self.discount1 = Discount.objects.create(
            amount=10,
            code="discountcode1",
        )
        self.discount1.consultants.set([self.consultant1_profile, self.consultant2_profile])

        self.discount2 = Discount.objects.create(
            amount=20,
            code="discountcode2",
        )
        self.discount2.consultants.set([self.consultant1_profile, ])

        # Cart consultant discounts
        self.cart_discount1 = CartDiscount.objects.create(
            cart=self.cart1,
            discount=self.discount1
        )

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
