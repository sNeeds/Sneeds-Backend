from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from abroadin.base.django.tests.generics import SampleGFKObjectMixIn
from abroadin.base.mixins.tests import TestBriefMethodMixin

from abroadin.apps.data.applydata.models import GradeChoices

from ...data.account.models import Major, University, Country
from ...data.account.tests.fixtures import UniversityFixtures, MajorFixtures, CountryFixtures
from ...data.applydata.models import RegularLanguageCertificate, GREGeneralCertificate, LanguageCertificate, \
    Publication, Education, GradeChoices, Grade, SemesterYear
from ...data.applydata.tests.fixtures import SemesterYearFixtures, GradeFixtures, EducationFixtures, \
    PublicationFixtures, RegularLCFixtures, GREGeneralFixtures

User = get_user_model()


class ApplyProfileTestBase(SemesterYearFixtures, GradeFixtures, EducationFixtures, PublicationFixtures,
                           RegularLCFixtures, GREGeneralFixtures,
                           UniversityFixtures, CountryFixtures, MajorFixtures,
                           SampleGFKObjectMixIn,
                           TestBriefMethodMixin,
                           APITestCase,
                           ):

    def setUp(self) -> None:
        # print('ApplyProfileTestBase setup')
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

        # ----- Setup ------

        self.client = APIClient()
