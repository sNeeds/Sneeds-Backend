from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from abroadin.apps.store.storeBase.models import TimeSlotSale, SoldTimeSlotSale

from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()



class StoreTests(CustomAPITestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()

        # Setup ------
        self.client = APIClient()

    def test_time_slot_sales_to_sold_time_slot_sales_working(self):
        class TempTimeSlotSale:
            def __init__(self, consultant, price, start_time, end_time):
                self.consultant = consultant
                self.price = price
                self.start_time = start_time
                self.end_time = end_time

        time_slot_sales_qs = TimeSlotSale.objects.all()

        temp_time_slot_sales_list = []
        for obj in time_slot_sales_qs:
            temp_time_slot_sales_list.append(
                TempTimeSlotSale(obj.consultant, obj.price, obj.start_time, obj.end_time)
            )

        time_slot_sales_qs.set_time_slot_sold(self.user1)

        self.assertEqual(TimeSlotSale.objects.all().count(), 0)
        for obj in temp_time_slot_sales_list:
            self.assertEqual(
                SoldTimeSlotSale.objects.filter(
                    consultant=obj.consultant,
                    price=obj.price,
                    start_time=obj.start_time,
                    end_time=obj.end_time,
                    sold_to=self.user1
                ).count(),
                1
            )

