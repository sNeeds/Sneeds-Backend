from abroadin.apps.applyprofile.models import ApplyProfile

from ...form.models import StudentDetailedInfo
from ...tests.base import EstimationTestBase


class SimilarProfilesTestsBase(EstimationTestBase):
    def setUp(self):
        super().setUp()

        self.form_1 = StudentDetailedInfo.objects.create(
            user=self.user1,
            age=20,
            gender=StudentDetailedInfo.GenderChoices.MALE,
            related_work_experience=0,
            academic_break=0,
            powerful_recommendation=False
        )

        self.profile_1 = ApplyProfile.objects.create(
            name="profile 1",
            gap=5,
        )

        self.profile_2 = ApplyProfile.objects.create(
            name="profile 2",
            gap=0
        )
