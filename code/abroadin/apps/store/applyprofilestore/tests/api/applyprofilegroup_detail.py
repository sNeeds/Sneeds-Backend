from rest_framework import status

from .base import ApplyProfileStoreAPITestBase
from ...models import ApplyProfileGroup
from ...values import MAX_ALLOWED_APPLY_PROFILES


class ApplyProfileGroupDetailTest(ApplyProfileStoreAPITestBase):

    def setUp(self):
        super().setUp()

    def _test_apply_profile_group_detail(self, *args, **kwargs):
        return self._endpoint_test_method('store.applyprofilestore:apply-profile-group-detail', *args, **kwargs)

    def test_apply_profile_group_detail_get_200(self):
        res = self._test_apply_profile_group_detail('get', self.app_profile_group1.user,
                                                    status.HTTP_200_OK, self.app_profile_group1.id)

    def test_apply_profile_group_detail_delete_204(self):
        user = self.app_profile_group1.user
        n = ApplyProfileGroup.objects.filter(user=user).count()
        res = self._test_apply_profile_group_detail('delete', user,
                                                    status.HTTP_204_NO_CONTENT, self.app_profile_group1.id)

        self.assertEqual(ApplyProfileGroup.objects.filter(user=user).count(), n-1)

    def test_apply_profile_group_detail_get_401(self):
        res = self._test_apply_profile_group_detail('get', None, status.HTTP_401_UNAUTHORIZED,
                                                    self.app_profile_group1.id)

    def test_apply_profile_group_detail_get_403(self):
        res = self._test_apply_profile_group_detail('get', self.user2, status.HTTP_403_FORBIDDEN,
                                                    self.app_profile_group1.id)

    def test_apply_profile_group_detail_post_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'user': self.user2.id,
        }
        res = self._test_apply_profile_group_detail('post', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                    self.app_profile_group1.id, data=data)

    def test_apply_profile_group_detail_put_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'user': self.user2,
        }
        res = self._test_apply_profile_group_detail('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                    self.app_profile_group1.id)

    def test_apply_profile_group_detail_patch_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'user': self.user2,
        }
        res = self._test_apply_profile_group_detail('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                    self.app_profile_group1.id)
