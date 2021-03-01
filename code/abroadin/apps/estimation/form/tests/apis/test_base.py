from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.applydata.models import GradeChoices, LanguageCertificate, Publication
from abroadin.apps.estimation.form.tests.fixtures import WantToApplyFixturesMixin, StudentDetailedInfoFixturesMixin
from abroadin.apps.estimation.tests.base import EstimationTestBase
from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.data.applydata.tests.fixtures import EducationFixturesMixin, RegularLCFixturesMixin, \
    PublicationFixturesMixin, GREGeneralFixturesMixin

User = get_user_model()


class FormAPITestBase(WantToApplyFixturesMixin, StudentDetailedInfoFixturesMixin,
                      EducationFixturesMixin, PublicationFixturesMixin,
                      RegularLCFixturesMixin, GREGeneralFixturesMixin,
                      EstimationTestBase):

    def setUp(self):
        super().setUp()
