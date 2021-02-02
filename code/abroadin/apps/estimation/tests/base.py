from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from abroadin.apps.data.account.models import University, Major, Country
from abroadin.apps.estimation.form.models import SemesterYear, StudentDetailedInfo, Grade
from abroadin.base.mixins.tests import TestBriefMethodMixin
from abroadin.apps.data.applydata.models import GradeChoices

User = get_user_model()


class EstimationBaseTest(TestBriefMethodMixin, APITestCase):
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

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234", first_name="User 3")
        self.user3.is_admin = False
        self.user3.is_email_verified = True
        self.user3.save()

        # ------- Countries -------

        self.country1 = Country.objects.create(
            name="country1",
            search_name="country1",
            slug="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            search_name="country2",
            slug="country2",
            picture=None
        )

        self.country3 = Country.objects.create(
            name="country3",
            search_name="country3",
            slug="country3",
            picture=None
        )

        # ------- Universities -------

        self.university1 = University.objects.create(
            name="university1",
            search_name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            rank=80
        )

        self.university2 = University.objects.create(
            name="university2",
            search_name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            rank=800
        )

        self.university3 = University.objects.create(
            name="university3",
            search_name="university3",
            country=self.country3,
            description="Test desc3",
            picture=None,
            rank=1500
        )

        # ------- Majors -------

        self.major1 = Major.objects.create(
            name="Foo major 1",
            search_name="Foo major 1",
            description="Foo major 1",
        )

        self.major2 = Major.objects.create(
            name="Foo major 2",
            search_name="Foo major 2",
            description="Foo major 2",
        )

        self.major3 = Major.objects.create(
            name="Foo major 3",
            search_name="Foo major 3",
            description="Foo major 3",
        )

        # ------- Semester Years -------

        self.semester_year1 = SemesterYear.objects.create(
            year=2022,
            semester=SemesterYear.SemesterChoices.SPRING
        )
        self.semester_year2 = SemesterYear.objects.create(
            year=2022,
            semester=SemesterYear.SemesterChoices.WINTER
        )
        self.semester_year3 = SemesterYear.objects.create(
            year=2023,
            semester=SemesterYear.SemesterChoices.FALL
        )

        # ------- Grade Objects -------

        self.grade_bachelor = Grade.objects.create(
            name=GradeChoices.BACHELOR
        )

        self.grade_master = Grade.objects.create(
            name=GradeChoices.MASTER
        )

        self.grade_phd = Grade.objects.create(
            name=GradeChoices.PHD
        )

        self.grade_postdoc = Grade.objects.create(
            name=GradeChoices.POST_DOC
        )

        # ----- Setup ------

        self.client = APIClient()
