from abroadin.apps.store.applyprofilestore.tests.base import ApplyProfileStoreTestBase
from abroadin.apps.store.applyprofilestore.tests.fixtures import SoldApplyProfileGroupFixturesMixin, \
    ApplyProfileGroupFixturesMixin
from abroadin.base.mixins.tests import TestBriefMethodMixin


class ApplyProfileStoreAPITestBase(ApplyProfileGroupFixturesMixin, SoldApplyProfileGroupFixturesMixin,
                                   ApplyProfileStoreTestBase, TestBriefMethodMixin):
    def setUp(self):
        super().setUp()
