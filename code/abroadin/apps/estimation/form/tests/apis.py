from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest

User = get_user_model()


class StudentDetailedInfoTests(EstimationBaseTest):

    def setUp(self):
        super().setUp()

    def test_form_creation_201(self):
        url = reverse('estimation.form:student-detailed-info')
        client = self.client
        client.force_login(self.user1)

        # response = client.post(url)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # payload = {
        # }
        #
        # response = client.post(url, payload)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
