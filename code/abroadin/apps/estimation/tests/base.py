from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from abroadin.apps.data.globaldata.tests.fixtures import UniversityFixturesMixin, CountryFixturesMixin, MajorFixturesMixin
from abroadin.apps.data.applydata.tests.fixtures import EducationFixturesMixin, RegularLCFixturesMixin, \
    SemesterYearFixturesMixin, PublicationFixturesMixin, GREGeneralFixturesMixin, GradeFixturesMixin
from abroadin.base.django.tests.generics import SampleGFKObjectMixIn
from abroadin.base.mixins.tests import TestBriefMethodMixin

User = get_user_model()


class EstimationTestBase(UniversityFixturesMixin, CountryFixturesMixin, MajorFixturesMixin,
                         SemesterYearFixturesMixin, GradeFixturesMixin,
                         SampleGFKObjectMixIn,
                         TestBriefMethodMixin, APITestCase):
    def setUp(self):
        super().setUp()

        # ------- Users -------

        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234", first_name="User 1")
        self.user1.is_admin = False
        self.user1.is_email_verified = True
        self.user1.save()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234", first_name="User 2")
        self.user2.is_admin = False
        self.user2.is_email_verified = True
        self.user2.save()

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234", first_name="User 3")
        self.user3.is_admin = False
        self.user3.is_email_verified = True
        self.user3.save()

        # ----- Setup ------

        self.client = APIClient()
