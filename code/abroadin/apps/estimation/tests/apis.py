from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient

from abroadin.apps.data.account.models import University, Major, Country

User = get_user_model()


class EstimationBaseTest(APITestCase):
    def setUp(self):
        # ------- Users -------

        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234", first_name="User 1")
        self.user1.is_admin = False

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234", first_name="User 3")
        self.user3.is_admin = False

        # ------- Countries -------

        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            picture=None
        )

        # ------- Universities -------

        self.university1 = University.objects.create(
            name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            slug="university1"
        )

        self.university2 = University.objects.create(
            name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            slug="university2"
        )

        # ------- Majors -------

        self.major1 = Major.objects.create(
            name="field of study1",
            description="Test desc1",
            picture=None,
            slug="field-of-study1"
        )

        self.major2 = Major.objects.create(
            name="field of study2",
            description="Test desc2",
            picture=None,
            slug="field-of-study2"
        )

        # ----- Setup ------

        self.client = APIClient()
