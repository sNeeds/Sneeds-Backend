from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient

from abroadin.base.mixins.tests import TestBriefMethodMixin

User = get_user_model()


class SocialAuthTestBase(APITestCase, TestBriefMethodMixin):
    def setUp(self):

        # ------- Users -------

        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234", first_name="User 1")
        self.user1.is_admin = False
        self.user1.is_email_verified = True
        self.user1.save()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False
        self.user2.is_email_verified = True
        self.user2.save()

        # ----- Setup ------

        self.client = APIClient()
