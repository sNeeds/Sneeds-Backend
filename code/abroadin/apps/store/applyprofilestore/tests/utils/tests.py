from abroadin.apps.store.applyprofilestore.tests.base import ApplyProfileStoreTestBase
from abroadin.apps.store.applyprofilestore.tests.fixtures import ApplyProfileGroupFixturesMixin, \
    SoldApplyProfileGroupFixturesMixin

from abroadin.apps.store.applyprofilestore.utils import get_user_bought_apply_profiles


class UtilsTests(ApplyProfileGroupFixturesMixin, SoldApplyProfileGroupFixturesMixin,
                 ApplyProfileStoreTestBase):

    def setUp(self):
        super().setUp()

    def test_user_bought_apply_profiles(self):
        sample_ap_id = self.app_profile_group1.apply_profiles.first().id
        self.assertNotIn(sample_ap_id, get_user_bought_apply_profiles(self.app_profile_group1.user).values_list('id', flat=True))
        sold_apply_profile_group = self.app_profile_group1.sell()
        self.assertIn(sample_ap_id, get_user_bought_apply_profiles(sold_apply_profile_group.sold_to).values_list('id', flat=True))
