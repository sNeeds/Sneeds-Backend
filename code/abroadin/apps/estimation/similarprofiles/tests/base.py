from django.contrib.auth import get_user_model

from abroadin.apps.applyprofile.models import ApplyProfile
from ...tests.base import EstimationBaseTest

User = get_user_model()


class SimilarProfilesBaseTests(EstimationBaseTest):
    def setUp(self):
        super().setUp()

        self.apply_profile_1 = ApplyProfile.objects.create(
            name="profile 1",
            gap=5,
        )
