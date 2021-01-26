from rest_framework.test import APITestCase

from ..models import Major, University, Country


class AccountTestBase(APITestCase):

    def setUp(self) -> None:

        super().setUp()

        # Countries -------
        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            search_name="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            search_name="country2",
            picture=None
        )

        self.country3 = Country.objects.create(
            name="country3",
            slug="country3",
            search_name="country3",
            picture=None
        )

        # Universities -------
        self.university1 = University.objects.create(
            name="university1",
            search_name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            rank=50,
        )

        self.university2 = University.objects.create(
            name="university2",
            search_name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            rank=150,
        )

        self.university3 = University.objects.create(
            name="university3",
            search_name="university3",
            country=self.country2,
            description="Test desc3",
            picture=None,
            rank=200,
        )

        # Field of Studies -------
        self.major1 = Major.objects.create(
            name="field of study1",
            search_name="field of study1",
            description="Test desc1",
        )

        self.major2 = Major.objects.create(
            name="field of study2",
            search_name="field of study2",
            description="Test desc2",
        )

        self.major3 = Major.objects.create(
            name="field of study3",
            search_name="field of study3",
            description="Test desc3",
        )