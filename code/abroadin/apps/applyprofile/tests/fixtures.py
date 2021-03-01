from abroadin.apps.applyprofile.models import Admission, ApplyProfile
from abroadin.apps.data.globaldata.tests.fixtures import MajorFixturesMixin, UniversityFixturesMixin
from abroadin.apps.data.applydata.tests.fixtures import GradeFixturesMixin
from abroadin.base.django.tests.generics import TestFixtureMixIn


class ApplyProfileFixturesMixin:

    def setUp(self) -> None:
        # print('apply profile fixture setup')
        super().setUp()

        self.applyprofile1 = ApplyProfile.objects.create(
            name='applyprofile1',
            gap=10,
        )

        self.applyprofile2 = ApplyProfile.objects.create(
            name='applyprofile2',
            gap=10,
        )

        self.applyprofile3 = ApplyProfile.objects.create(
            name='applyprofile3',
            gap=10,
        )

        self.applyprofile4 = ApplyProfile.objects.create(
            name='applyprofile4',
            gap=10,
        )

        self.applyprofile5 = ApplyProfile.objects.create(
            name='applyprofile5',
            gap=10,
        )

        self.applyprofile6 = ApplyProfile.objects.create(
            name='applyprofile6',
            gap=10,
        )

        self.applyprofile7 = ApplyProfile.objects.create(
            name='applyprofile7',
            gap=10,
        )

        self.applyprofile8 = ApplyProfile.objects.create(
            name='applyprofile8',
            gap=10,
        )

        self.applyprofile9 = ApplyProfile.objects.create(
            name='applyprofile9',
            gap=10,
        )


class AdmissionFixturesMixin:

    def setUp(self) -> None:
        # print('admission fixture setup')
        super().setUp()

        self.admission1for1 = Admission.objects.create(
            apply_profile=self.applyprofile1,
            major=self.major1,
            grade=self.bachelor_grade,
            destination=self.university1,
            accepted=False,
            scholarship=2000,
            enroll_year=2018,
            description='giivbkwfoewvnopibv',
        )

        self.admission2for1 = Admission.objects.create(
            apply_profile=self.applyprofile1,
            major=self.major2,
            grade=self.bachelor_grade,
            destination=self.university2,
            accepted=True,
            scholarship=3000,
            enroll_year=2018,
            description='sdbfspfkknvkv',
        )

        self.admission1for2 = Admission.objects.create(
            apply_profile=self.applyprofile2,
            major=self.major3,
            grade=self.master_grade,
            destination=self.university3,
            accepted=False,
            scholarship=2200,
            enroll_year=2019,
            description='giivbkwfoewvnopibv',
        )

        self.admission2for2 = Admission.objects.create(
            apply_profile=self.applyprofile2,
            major=self.major2,
            grade=self.master_grade,
            destination=self.university2,
            accepted=False,
            scholarship=800,
            enroll_year=2020,
            description='giivbkwfoewvnopibv',
        )