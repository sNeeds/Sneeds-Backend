from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient

from ..base import SocialAuthTestBase

User = get_user_model()


class SocialAuthFunctionTestBase(SocialAuthTestBase):
    def setUp(self):
        super().setUp()
