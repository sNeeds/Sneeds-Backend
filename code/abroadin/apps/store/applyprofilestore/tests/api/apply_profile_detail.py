from rest_framework import status

from abroadin.base.values import AccessibilityTypeChoices
from .base import ApplyProfileStoreAPITestBase


class ApplyProfileDetailAPITest(ApplyProfileStoreAPITestBase):
    def setUp(self) -> None:
        super().setUp()

    def _test_apply_profile_detail(self, *args, **kwargs):
        return self._endpoint_test_method('applyprofile:apply-profile-detail', *args, **kwargs)

    def test_apply_profile_detail_get_200_all(self):
        sample_ap_id = self.app_profile_group1.apply_profiles.first().id
        res = self._test_apply_profile_detail('get', self.user1, status.HTTP_200_OK,
                                              sample_ap_id)
        self.assertEqual(res['accessibility_type'], AccessibilityTypeChoices.PARTIAL)
        self.app_profile_group1.sell()

        res = self._test_apply_profile_detail('get', self.user1, status.HTTP_200_OK,
                                              sample_ap_id)
        self.assertEqual(res['accessibility_type'], AccessibilityTypeChoices.UNLOCKED)

