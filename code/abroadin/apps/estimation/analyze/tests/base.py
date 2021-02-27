from abroadin.apps.data.applydata.tests.fixtures import RegularLCFixturesMixin, EducationFixturesMixin, \
    PublicationFixturesMixin, GREGeneralFixturesMixin
from abroadin.apps.estimation.form.tests.fixtures import WantToApplyFixturesMixin, StudentDetailedInfoFixturesMixin

from abroadin.apps.estimation.tests.base import EstimationTestBase


class AnalyzeTestBase(WantToApplyFixturesMixin, StudentDetailedInfoFixturesMixin,
                      EducationFixturesMixin, PublicationFixturesMixin,
                      RegularLCFixturesMixin, GREGeneralFixturesMixin,
                      EstimationTestBase
                      ):

    def setUp(self) -> None:
        super().setUp()
