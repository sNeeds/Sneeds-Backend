from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.conf import settings

from abroadin.apps.data.globaldata.models import Country, University, Major
from abroadin.apps.store.carts.models import Cart

USER_DETAILED_INFO_BASE_PAYLOAD = {
    "first_name": "u1",
    "last_name": "u1u1",
    "age": 19,
    "marital_status": "married",
    "grade": "college",
    "university": "payamnoor",
    "total_average": "16.20",
    "degree_conferral_year": 2022,
    "major": "memari jolbak",
    "thesis_title": "kasht jolbak dar darya",
    "language_certificate": "ielts_academic",
    "language_certificate_overall": 50,
    "language_speaking": 50,
    "language_listening": 10,
    "language_writing": 50,
    "language_reading": 50,
    "mainland": "asia",
    "country": "america",
    "apply_grade": "college",
    "apply_major": "tashtak sazi",
    "comment": "HEllllo",
}

User = get_user_model()


class CustomAPITestCase(APITestCase):
    def setUp(self):
        # Configs
        settings.SKYROOM_API_KEY = None

        # Users -------
        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234", first_name="User 1")
        self.user1.is_admin = False

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234", first_name="User 3")
        self.user3.is_admin = False

        # Countries -------
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

        # Universities -------
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

        # Field of Studies -------
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

        # Setup ------
        self.client = APIClient()
