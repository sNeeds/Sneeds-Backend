from ...values import APPLY_PROFILE_PRICE_IN_DOLLAR

from .base import ApplyProfileStoreModelTestBase
from ...models import ApplyProfileGroup


class ApplyProfileStoreModelBasicTests(ApplyProfileStoreModelTestBase):

    def setUp(self):
        super().setUp()

    def test_create_through_custom_function_1(self):
        """
        basic creation
        """
        apply_profile_group = ApplyProfileGroup.objects.create_with_apply_profiles(
            user=self.user1,
            apply_profiles=[self.applyprofile1],
            price=10000,
        )

        self.assertEqual(apply_profile_group.price, 8000)

    def test_create_through_custom_function_2(self):
        """
        check price
        """
        apply_profile_group = ApplyProfileGroup.objects.create_with_apply_profiles(
            user=self.user1,
            apply_profiles=[self.applyprofile1, self.applyprofile2, self.applyprofile3]
        )

        self.assertEqual(apply_profile_group.price, 16000)

    def test_cal_price(self):
        res = ApplyProfileGroup.calculate_profiles_price([self.applyprofile1, self.applyprofile2, self.applyprofile3])
        self.assertEqual(res, 16000)

    def test_normal_price(self):
        self.assertEqual(self.app_profile_group2.normal_price, 24000)

    def test_sell_apply_profile_group(self):
        sold_apply_profile_group = self.app_profile_group1.sell()
        self.assertEqual(sold_apply_profile_group.price, 11000)
        self.assertEqual(sold_apply_profile_group.apply_profiles.count(), 2)
        self.assertEqual(sold_apply_profile_group.sold_to, self.app_profile_group1.user)
        self.assertFalse(ApplyProfileGroup.objects.filter(pk=self.app_profile_group1.id).exists())