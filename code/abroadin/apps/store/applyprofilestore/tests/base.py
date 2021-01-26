from abroadin.apps.applyprofile.models import ApplyProfile
from abroadin.apps.applyprofile.tests.base import ApplyProfileTestBase

from ...tests.base import StoreBaseTest
from ..models import ApplyProfileGroup


class ApplyProfileStoreTestBase(StoreBaseTest, ApplyProfileTestBase):
    def setUp(self):
        StoreBaseTest.setUp(self)
        ApplyProfileTestBase.setUp(self)

        self.app_profile_group1 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )

        self.app_profile_group2 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )

        self.app_profile_group3 = ApplyProfileGroup.objects.create(
            user=self.user2,
            active=True,
            price=4,
        )

        self.app_profile_group1.apply_profiles.set([self.applyprofile1, self.applyprofile2])

        self.app_profile_group2.apply_profiles.set([self.applyprofile4, self.applyprofile5, self.applyprofile6])

        self.app_profile_group3.apply_profiles.set([self.applyprofile2, self.applyprofile3,
                                                    self.applyprofile4, self.applyprofile5])





