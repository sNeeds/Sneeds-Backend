from django.contrib.contenttypes.models import ContentType

from abroadin.apps.applyprofile.models import ApplyProfile, Admission
from abroadin.apps.data.account.models import Country, University
from abroadin.apps.data.applydata.models import Grade, Education

from ...form.models import StudentDetailedInfo, WantToApply
from ...tests.base import EstimationBaseTest


class SimilarProfilesBaseTests(EstimationBaseTest):
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
