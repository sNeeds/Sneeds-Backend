from rest_framework import status

from .base import ApplyProfileAPIsTestBase


class ApplyProfileListAPITest(ApplyProfileAPIsTestBase):
    def setUp(self) -> None:
        super().setUp()

    def _test_apply_profile_list(self, *args, **kwargs):
        return self._endpoint_test_method('applyprofile:apply-profile-list', *args, **kwargs)

    def test_apply_profile_list_get_200(self):
        res = self._test_apply_profile_list('get', self.user1, status.HTTP_200_OK)