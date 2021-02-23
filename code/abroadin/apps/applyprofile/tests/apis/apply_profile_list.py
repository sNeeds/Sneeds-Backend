from rest_framework import status

from .base import ApplyProfileAPIsTestBase


class ApplyProfileListAPITest(ApplyProfileAPIsTestBase):
    def setUp(self) -> None:
        super().setUp()

    def _test_apply_profile_list(self, *args, **kwargs):
        return self._endpoint_test_method('applyprofile:apply-profile-list', *args, **kwargs)

    def test_apply_profile_list_get_200(self):
        res = self._test_apply_profile_list('get', self.user1, status.HTTP_200_OK)
        self.assertEqual(len(res['results']), 9)

    def test_app_profile_list_post_405(self):
        res = self._test_apply_profile_list('post', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={})

    def test_app_profile_list_delete_405(self):
        res = self._test_apply_profile_list('delete', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_app_profile_list_put_405(self):
        res = self._test_apply_profile_list('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={})

    def test_app_profile_list_patch_405(self):
        res = self._test_apply_profile_list('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={})
