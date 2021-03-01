from django.contrib.auth import get_user_model

from abroadin.apps.data.applydata.tests.fixtures import EducationFixturesMixin, PublicationFixturesMixin, \
    RegularLCFixturesMixin, GREGeneralFixturesMixin
from abroadin.apps.estimation.form.tests.fixtures import WantToApplyFixturesMixin, StudentDetailedInfoFixturesMixin
from abroadin.apps.estimation.tests.base import EstimationTestBase


User = get_user_model()


class EstimationsAppTestsBase(WantToApplyFixturesMixin, StudentDetailedInfoFixturesMixin,
                              EducationFixturesMixin, PublicationFixturesMixin,
                              RegularLCFixturesMixin, GREGeneralFixturesMixin,
                              EstimationTestBase):

    def setUp(self):
        super().setUp()
