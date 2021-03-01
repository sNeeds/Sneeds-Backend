from abroadin.apps.applyprofile.tests.fixtures import AdmissionFixturesMixin, ApplyProfileFixturesMixin
from abroadin.apps.data.globaldata.tests.fixtures import CountryFixturesMixin, MajorFixturesMixin, UniversityFixturesMixin
from abroadin.base.django.tests.generics import SampleGFKObjectMixIn

from ...tests.base import StoreBaseTest

from abroadin.apps.data.applydata.tests.fixtures import SemesterYearFixturesMixin, GradeFixturesMixin, \
    EducationFixturesMixin, PublicationFixturesMixin, RegularLCFixturesMixin, GREGeneralFixturesMixin


class ApplyProfileStoreTestBase(AdmissionFixturesMixin, ApplyProfileFixturesMixin,
                                EducationFixturesMixin, PublicationFixturesMixin,
                                RegularLCFixturesMixin, GREGeneralFixturesMixin,
                                SemesterYearFixturesMixin, GradeFixturesMixin,
                                UniversityFixturesMixin, CountryFixturesMixin, MajorFixturesMixin,
                                SampleGFKObjectMixIn,
                                StoreBaseTest):
    def setUp(self):
        super().setUp()
