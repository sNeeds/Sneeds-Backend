from abroadin.apps.store.applyprofilestore.tests.base import ApplyProfileStoreTestBase
from abroadin.base.mixins.tests import TestBriefMethodMixin


class ApplyProfileStoreAPITestBase(ApplyProfileStoreTestBase, TestBriefMethodMixin):
    def setUp(self):
        super().setUp()
