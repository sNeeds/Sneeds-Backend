from ..base import ApplyProfileTestBase
from ..fixtures import AdmissionFixturesMixin, ApplyProfileFixturesMixin
from ...models import Admission, ApplyProfile


class ApplyProfileAPIsTestBase(AdmissionFixturesMixin, ApplyProfileFixturesMixin, ApplyProfileTestBase,):

    def setUp(self) -> None:
        # print('ApplyProfileAPIsTestBase setup')
        super().setUp()
