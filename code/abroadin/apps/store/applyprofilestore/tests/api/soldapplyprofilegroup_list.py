from rest_framework import status

from .base import ApplyProfileStoreAPITestBase
from ...models import ApplyProfileGroup
from ...values import MAX_ALLOWED_APPLY_PROFILES


class SoldApplyProfileGroupListTest(ApplyProfileStoreAPITestBase):

    def setUp(self):
        super().setUp()

    def _test_sold_apply_profile_group_list(self, *args, **kwargs):
        return self._endpoint_test_method('store.applyprofilestore:sold-apply-profile-group-list', *args, **kwargs)

    def test_sold_apply_profile_group_list_get_200(self):
        res = self._test_sold_apply_profile_group_list('get', self.user1,
                                                       status.HTTP_200_OK)
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]['apply_profiles']), 2)
        self.assertEqual(len(res[1]['apply_profiles']), 3)

    def test_sold_apply_profile_group_list_get_401(self):
        res = self._test_sold_apply_profile_group_list('get', None, status.HTTP_401_UNAUTHORIZED)

    def test_sold_apply_profile_group_list_post_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'sold_to': self.user2.id,
        }
        res = self._test_sold_apply_profile_group_list('post', self.user2, status.HTTP_405_METHOD_NOT_ALLOWED,
                                                       data=data)

    def test_sold_apply_profile_group_list_delete_405(self):
        res = self._test_sold_apply_profile_group_list('delete', self.user1,
                                                       status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_sold_apply_profile_group_list_put_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'sold_to': self.user2,
        }
        res = self._test_sold_apply_profile_group_list('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_sold_apply_profile_group_list_patch_405(self):
        data = {
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id],
            'sold_to': self.user2,
        }
        res = self._test_sold_apply_profile_group_list('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED)
