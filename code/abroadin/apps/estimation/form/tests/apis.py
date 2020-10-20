from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest

User = get_user_model()


class StudentDetailedInfoTests(EstimationBaseTest):

    def setUp(self):
        super().setUp()

    def create_form(self, user, expected_status):
        url = reverse('estimation.form:student-detailed-info-list')
        client = self.client

        if user:
            client.force_login(user)

        response = client.post(url)
        self.assertEqual(response.status_code, expected_status)

    def test_form_creation_201(self):
        self.create_form(None, status.HTTP_201_CREATED)
        self.create_form(self.user1, status.HTTP_201_CREATED)

    def test_form_creation_400(self):
        self.create_form(self.user1, status.HTTP_201_CREATED)
        self.create_form(self.user1, status.HTTP_400_BAD_REQUEST)
