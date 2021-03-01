from abroadin.apps.store.applyprofilestore.models import ApplyProfileGroup, SoldApplyProfileGroup


class ApplyProfileGroupFixturesMixin:
    def setUp(self):

        super().setUp()

        self.app_profile_group1 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )
        self.app_profile_group1.apply_profiles.set([self.applyprofile1])

        self.app_profile_group2 = ApplyProfileGroup.objects.create(
            user=self.user1,
            active=True,
            price=4,
        )
        self.app_profile_group2.apply_profiles.set([self.applyprofile2, self.applyprofile3,])

        self.app_profile_group3 = ApplyProfileGroup.objects.create(
            user=self.user2,
            active=True,
            price=4,
        )
        self.app_profile_group3.apply_profiles.set([self.applyprofile2, self.applyprofile3,
                                                    self.applyprofile4, self.applyprofile5])


class SoldApplyProfileGroupFixturesMixin:
    def setUp(self):

        super().setUp()

        self.sold_app_profile_group1 = SoldApplyProfileGroup.objects.create(
            sold_to=self.user1,
            price=4,
        )

        self.sold_app_profile_group2 = SoldApplyProfileGroup.objects.create(
            sold_to=self.user1,
            price=4,
        )

        self.sold_app_profile_group3 = SoldApplyProfileGroup.objects.create(
            sold_to=self.user2,
            price=4,
        )

        self.sold_app_profile_group1.apply_profiles.set([self.applyprofile4])

        self.sold_app_profile_group2.apply_profiles.set([self.applyprofile5, self.applyprofile6])

        self.sold_app_profile_group3.apply_profiles.set([self.applyprofile1, self.applyprofile8])
