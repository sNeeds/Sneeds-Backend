from rest_framework import status

from .base import ApplyProfileStoreAPITestBase
from ...values import MAX_ALLOWED_APPLY_PROFILES


class ApplyProfileGroupListTest(ApplyProfileStoreAPITestBase):

    def setUp(self):
        super().setUp()

    def _test_apply_profile_group_list(self, *args, **kwargs):
        return self._endpoint_test_method('store.applyprofilestore:apply-profile-group-list', *args, **kwargs)

    def test_apply_profile_group_list_get_200(self):
        res = self._test_apply_profile_group_list('get', self.user1, status.HTTP_200_OK)
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]['apply_profiles']), 2)
        self.assertEqual(len(res[1]['apply_profiles']), 3)

    def test_apply_profile_group_list_get_200_2(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)
        self.assertEqual(len(res[0]['apply_profiles']), 4)

    def test_apply_profile_group_list_get_401_1(self):
        res = self._test_apply_profile_group_list('get', None, status.HTTP_401_UNAUTHORIZED)

    def test_apply_profile_group_list_post_201(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

        data = {
            'user': self.user2.id,
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id]
        }

        res = self._test_apply_profile_group_list('post', self.user2, status.HTTP_201_CREATED, data=data)
        self.assertEqual(len(res['apply_profiles']), 2)

        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 2)

    def test_apply_profile_group_list_post_400_1(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

        apply_profiles = []

        for i in range(1, MAX_ALLOWED_APPLY_PROFILES+2):
            apply_profiles.append(getattr(self, 'applyprofile'+str(i)).id)

        data = {
            'user': self.user2.id,
            'apply_profiles': apply_profiles
        }

        res = self._test_apply_profile_group_list('post', self.user2, status.HTTP_400_BAD_REQUEST, data=data)

        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

    def test_apply_profile_group_list_post_400_2(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

        data = {
            'user': self.user1.id,
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id]
        }

        res = self._test_apply_profile_group_list('post', self.user2, status.HTTP_400_BAD_REQUEST, data=data)

        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

    def test_apply_profile_group_list_post_401_2(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

        data = {
            'user': self.user2.id,
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id]
        }

        res = self._test_apply_profile_group_list('post', None, status.HTTP_401_UNAUTHORIZED, data=data)

        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

    def test_apply_profile_group_list_put_405(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

        data = {
            'user': self.user2.id,
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id]
        }

        res = self._test_apply_profile_group_list('put', self.user2, status.HTTP_405_METHOD_NOT_ALLOWED, data=data)

        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

    def test_apply_profile_group_list_patch_405(self):
        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)

        data = {
            'user': self.user2.id,
            'apply_profiles': [self.applyprofile1.id, self.applyprofile2.id]
        }

        res = self._test_apply_profile_group_list('patch', self.user2, status.HTTP_405_METHOD_NOT_ALLOWED, data=data)

        res = self._test_apply_profile_group_list('get', self.user2, status.HTTP_200_OK)
        self.assertEqual(len(res), 1)





