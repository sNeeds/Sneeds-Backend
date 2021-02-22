from rest_framework import status

from .base import ApplyProfileStoreAPITestBase
from ...models import ApplyProfileGroup
from ...values import MAX_ALLOWED_APPLY_PROFILES


class SoldApplyProfileGroupDetailTest(ApplyProfileStoreAPITestBase):

    def setUp(self):
        super().setUp()

    def _test_sold_apply_profile_group_detail(self, *args, **kwargs):
        return self._endpoint_test_method('store.applyprofilestore:sold-apply-profile-group-detail', *args, **kwargs)

    def test_sold_apply_profile_group_detail_get_200(self):
        res = self._test_sold_apply_profile_group_detail('get', self.sold_app_profile_group1.sold_to,
                                                         status.HTTP_200_OK, self.sold_app_profile_group1.id)

    def test_sold_apply_profile_group_detail_delete_405(self):
        res = self._test_sold_apply_profile_group_detail('delete', self.sold_app_profile_group1.sold_to,
                                                         status.HTTP_405_METHOD_NOT_ALLOWED,
                                                         self.sold_app_profile_group1.id)

    def test_sold_apply_profile_group_detail_get_401(self):
        res = self._test_sold_apply_profile_group_detail('get', None, status.HTTP_401_UNAUTHORIZED,
                                                         self.sold_app_profile_group1.id)

    def test_sold_apply_profile_group_detail_get_403(self):
        res = self._test_sold_apply_profile_group_detail('get', self.user2, status.HTTP_403_FORBIDDEN,
                                                         self.sold_app_profile_group1.id)

    def test_sold_apply_profile_group_detail_post_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'sold_to': self.user2.id,
        }
        res = self._test_sold_apply_profile_group_detail('post', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                         self.sold_app_profile_group1.id, data=data)

    def test_sold_apply_profile_group_detail_put_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'sold_to': self.user2,
        }
        res = self._test_sold_apply_profile_group_detail('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                         self.sold_app_profile_group1.id)

    def test_sold_apply_profile_group_detail_patch_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'sold_to': self.user2,
        }
        res = self._test_sold_apply_profile_group_detail('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                         self.sold_app_profile_group1.id)
