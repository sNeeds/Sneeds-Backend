from rest_framework import status

from .base import ApplyProfileAPIsTestBase


class ApplyProfileDetailAPITest(ApplyProfileAPIsTestBase):
    def setUp(self) -> None:
        print('ApplyProfileDetailAPITest setup')
        super().setUp()

    def _test_apply_profile_detail(self, *args, **kwargs):
        return self._endpoint_test_method('applyprofile:apply-profile-detail', *args, **kwargs)

    def test_apply_profile_detail_get_200(self):
        res = self._test_apply_profile_detail('get', self.user1, status.HTTP_200_OK,
                                              self.applyprofile1.id)

    def test_app_profile_detail_post_405(self):
        res = self._test_apply_profile_detail('post', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              self.applyprofile1.id, data={})

    def test_app_profile_detail_delete_405(self):
        res = self._test_apply_profile_detail('delete', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              self.applyprofile1.id)

    def test_app_profile_detail_put_405(self):
        res = self._test_apply_profile_detail('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              self.applyprofile1.id, data={})

    def test_app_profile_detail_patch_405(self):
        res = self._test_apply_profile_detail('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                              self.applyprofile1.id, data={})
