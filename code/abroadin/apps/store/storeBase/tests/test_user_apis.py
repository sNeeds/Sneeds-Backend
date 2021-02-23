from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.datetime_safe import datetime
from rest_framework import status, serializers
from rest_framework.test import APIClient

from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class StoreTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        # Setup ------
        self.client = APIClient()
