from ..base import ApplyProfileTestBase
from ..fixtures import AdmissionFixtures, ApplyProfileFixtures
from ...models import Admission, ApplyProfile


class ApplyProfileAPIsTestBase(AdmissionFixtures, ApplyProfileFixtures, ApplyProfileTestBase,):

    def setUp(self) -> None:
        # print('ApplyProfileAPIsTestBase setup')
        super().setUp()
