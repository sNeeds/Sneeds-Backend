from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from sNeeds.apps.store.discounts.models import Discount, CartDiscount
from sNeeds.apps.store.storeBase.models import TimeSlotSale, SoldTimeSlotSale

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

