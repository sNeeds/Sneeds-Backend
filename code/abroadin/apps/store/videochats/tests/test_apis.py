from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from abroadin.apps.store.storeBase.models import SoldTimeSlotSale
from abroadin.apps.store.videochats.models import Room
from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class VideoChatTests(CustomAPITestCase):
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

        self.room1 = Room.objects.create(
            sold_time_slot=self.sold_time_slot_sale1,
        )
        self.room2 = Room.objects.create(
            sold_time_slot=self.sold_time_slot_sale2
        )

        # Setup ------
        self.client = APIClient()

    def test_rooms_list_get_success(self):
        client = self.client
        url = reverse("videochat:room-list")

        client.login(email="u1@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            1
        )

        client.login(email="u2@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            1
        )

        client.login(email="c1@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            2
        )

        Room.objects.create(
            sold_time_slot=self.sold_time_slot_sale3
        )
        client.login(email="u2@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            2
        )

        Room.objects.all().delete()
        client.login(email="u1@g.com", password="user1234")
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            0
        )

    def test_rooms_list_get_filter_by_sold_time_slot(self):
        client = self.client
        client.login(email="u1@g.com", password="user1234")

        url = "%s?%s=%s" % (
            reverse("videochat:room-list"),
            "sold_time_slot",
            self.sold_time_slot_sale1.id
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("sold_time_slot"), self.sold_time_slot_sale1.id)

        url = "%s?%s=%s" % (
            reverse("videochat:room-list"),
            "sold_time_slot",
            self.sold_time_slot_sale3.id
        )
        response = client.get(url, format='json')

        # TODO: This should be HTTP_403
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rooms_list_authenticate_permission(self):
        client = self.client
        url = reverse("videochat:room-list")

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rooms_detail_get_success(self):
        client = self.client
        url = reverse("videochat:room-detail", args=(self.room1.id,))

        self.room1.room_id = 10
        self.room1.user_id = 11
        self.room1.consultant_id = 12
        self.room1.user_login_url = "http://127.0.0.1:8000/"
        self.room1.consultant_login_url = "http://127.0.0.1:8000/c"
        self.room1.save()
        self.room1.refresh_from_db()

        # For user
        client.login(email="u1@g.com", password="user1234")
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), self.room1.id)
        self.assertEqual(data.get("sold_time_slot"), self.room1.sold_time_slot.id)
        self.assertEqual(data.get("login_url"), self.room1.user_login_url)
        self.assertEqual(
            data.get("start_time"),
            self.room1.sold_time_slot.start_time
        )
        self.assertEqual(
            data.get("end_time"),
            self.room1.sold_time_slot.end_time
        )

        # For consultant
        client.login(email="c1@g.com", password="user1234")
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), self.room1.id)
        self.assertEqual(data.get("sold_time_slot"), self.room1.sold_time_slot.id)
        self.assertEqual(data.get("login_url"), self.room1.consultant_login_url)
        self.assertEqual(
            data.get("start_time"),
            self.room1.sold_time_slot.start_time
        )
        self.assertEqual(
            data.get("end_time"),
            self.room1.sold_time_slot.end_time
        )

    def test_rooms_detail_get_permission_denied(self):
        client = self.client
        url = reverse("videochat:room-detail", args=(self.room1.id,))

        # For user
        client.login(email="u2@g.com", password="user1234")
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rooms_detail_get_unauthorized(self):
        client = self.client
        url = reverse("videochat:room-detail", args=(self.room1.id,))

        # For user
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
