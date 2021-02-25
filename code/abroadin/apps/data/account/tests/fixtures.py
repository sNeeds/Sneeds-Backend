from abroadin.apps.applyprofile.models import Admission
from abroadin.apps.data.account.models import Country, Major, University
from abroadin.apps.data.applydata.models import SemesterYear
from abroadin.base.django.tests.generics import TestFixtureMixIn


class MajorFixtures:

    def setUp(self) -> None:
        super().setUp()

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

        self.major4 = Major.objects.create(
            name="field of study4",
            search_name="field of study4",
            description="Test desc4",
        )

        self.major5 = Major.objects.create(
            name="field of study5",
            search_name="field of study5",
            description="Test desc5",
        )

        self.major6 = Major.objects.create(
            name="field of study6",
            search_name="field of study6",
            description="Test desc6",
        )


class CountryFixtures:

    def setUp(self) -> None:
        super().setUp()

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

        self.country4 = Country.objects.create(
            name="country4",
            slug="country4",
            search_name="country4",
            picture=None
        )

        self.country5 = Country.objects.create(
            name="country5",
            slug="country5",
            search_name="country5",
            picture=None
        )

        self.country6 = Country.objects.create(
            name="country6",
            slug="country6",
            search_name="country6",
            picture=None
        )

        self.country7 = Country.objects.create(
            name="country7",
            slug="country7",
            search_name="country7",
            picture=None
        )


class UniversityFixtures:

    def setUp(self) -> None:
        super().setUp()

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

        self.university4 = University.objects.create(
            name="university4",
            search_name="university4",
            country=self.country3,
            description="Test desc4",
            picture=None,
            rank=250,
        )

        self.university5 = University.objects.create(
            name="university5",
            search_name="university5",
            country=self.country5,
            description="Test desc5",
            picture=None,
            rank=300,
        )

        self.university6 = University.objects.create(
            name="university6",
            search_name="university6",
            country=self.country4,
            description="Test desc6",
            picture=None,
            rank=350,
        )
