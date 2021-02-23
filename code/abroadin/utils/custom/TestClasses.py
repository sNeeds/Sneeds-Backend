from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.conf import settings

from abroadin.apps.data.globaldata.models import Country, University, Major
from abroadin.apps.store.carts.models import Cart
from abroadin.apps.users.consultants.models import ConsultantProfile, StudyInfo
from abroadin.apps.store.storeBase.models import TimeSlotSale, SoldTimeSlotSale

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
        self.user1.set_user_type_student()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False
        self.user2.set_user_type_student()

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234", first_name="User 3")
        self.user3.is_admin = False
        self.user3.set_user_type_student()

        user_1_detailed_info_payload = USER_DETAILED_INFO_BASE_PAYLOAD
        user_1_detailed_info_payload['user'] = self.user1
        self.user1_student_detailed_info = StudentDetailedInfo.objects.create(**user_1_detailed_info_payload)

        user_2_detailed_info_payload = USER_DETAILED_INFO_BASE_PAYLOAD
        user_2_detailed_info_payload['user'] = self.user2
        self.user2_student_detailed_info = StudentDetailedInfo.objects.create(**user_2_detailed_info_payload)

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

        # Consultants -------
        self.consultant1 = User.objects.create_user(email="c1@g.com", password="user1234")
        self.consultant1.is_admin = False
        self.consultant1.set_user_type_consultant()
        self.consultant1_profile = ConsultantProfile.objects.create(
            user=self.consultant1,
            bio="bio1",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant1",
            active=True,
            time_slot_price=100
        )

        StudyInfo.objects.create(
            consultant=self.consultant1_profile,
            university=self.university1,
            major=self.major1,
            grade="bachelor",
            order=1
        )
        StudyInfo.objects.create(
            consultant=self.consultant1_profile,
            university=self.university2,
            major=self.major1,
            grade="master",
            order=1
        )

        self.consultant2 = User.objects.create_user(email="c2@g.com", password="user1234")
        self.consultant2.is_admin = False
        self.consultant2.set_user_type_consultant()
        self.consultant2_profile = ConsultantProfile.objects.create(
            user=self.consultant2,
            bio="bio2",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant2",
            active=True,
            time_slot_price=80
        )

        # TimeSlotSales -------
        self.time_slot_sale1 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale2 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=2),
            end_time=timezone.now() + timezone.timedelta(hours=3),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale3 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale33 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale4 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant2_profile.time_slot_price
        )
        self.time_slot_sale5 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=7),
            end_time=timezone.now() + timezone.timedelta(hours=8),
            price=self.consultant2_profile.time_slot_price
        )

        # SoldTimeSlotSales -------
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

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        # Setup ------
        self.client = APIClient()
