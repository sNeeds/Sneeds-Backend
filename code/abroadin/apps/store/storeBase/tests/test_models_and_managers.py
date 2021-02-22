from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class StoreTests(CustomAPITestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()

        # Setup ------
        self.client = APIClient()
