from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from abroadin.apps.users.consultants.models import ConsultantProfile, StudyInfo

from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()



class ConsultantTests(CustomAPITestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()

        # Setup ------
        self.client = APIClient()

    def test_consultant_profile_list_success(self):
        client = self.client
        url = reverse("consultant:consultant-profile-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data.get("results")),
            len(ConsultantProfile.objects.all())
        )

    def test_consultant_profile_list_order_by_rate_success(self):
        client = self.client
        url = "%s?%s=%s" % (
            reverse("consultant:consultant-profile-list"),
            "ordering",
            "rate",
        )

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("results")[0].get("id"),
            self.consultant1_profile.id
        )
        self.assertEqual(
            response.data.get("results")[1].get("id"),
            self.consultant2_profile.id
        )

    # TODO: Add filter by uni, country and field

    def test_consultant_profile_detail_success(self):
        client = self.client
        c1 = self.consultant1_profile
        url = reverse("consultant:consultant-profile-detail", args=(c1.slug,))

        response = client.get(url, format="json")

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), c1.id)
        self.assertEqual(data.get("bio"), c1.bio)
        self.assertEqual(data.get("first_name"), c1.user.first_name)
        self.assertEqual(data.get("last_name"), c1.user.last_name)
        self.assertEqual(len(data.get("study_info")), len(StudyInfo.objects.filter(consultant=c1)))
        self.assertEqual(data.get("slug"), c1.slug)
        self.assertEqual(data.get("aparat_link"), c1.aparat_link)
        self.assertEqual(data.get("time_slot_price"), c1.time_slot_price)
        self.assertEqual(data.get("rate"), 3.2)
        self.assertEqual(data.get("active"), c1.active)
