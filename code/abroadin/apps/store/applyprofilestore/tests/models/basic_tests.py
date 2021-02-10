from ...values import APPLY_PROFILE_PRICE_IN_DOLLAR

from .base import ApplyProfileStoreModelTestBase
from ...models import ApplyProfileGroup


class ApplyProfileStoreModelBasicTests(ApplyProfileStoreModelTestBase):

    def setUp(self):
        super().setUp()

    def test_create_through_custom_function_1(self):
        apply_profile_group = ApplyProfileGroup.objects.create_with_apply_profiles(
            user=self.user1,
            apply_profiles=[self.applyprofile1],
            price=10000,
        )

        self.assertEqual(apply_profile_group.price, 8000)

    def test_create_through_custom_function_2(self):
        apply_profile_group = ApplyProfileGroup.objects.create_with_apply_profiles(
            user=self.user1,
            apply_profiles=[self.applyprofile1, self.applyprofile2, self.applyprofile3]
        )

        self.assertEqual(apply_profile_group.price, 16000)
