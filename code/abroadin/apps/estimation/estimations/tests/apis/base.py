from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear, \
    UniversityThrough, GradeChoices, Publication, RegularLanguageCertificate, LanguageCertificate
from abroadin.apps.data.account.models import Country, University, Major

User = get_user_model()


class EstimationsAppAPITests(EstimationBaseTest):

    def setUp(self):
        super().setUp()

    def _test_form_comments_detail(self, *args, **kwargs):
        return self._test_form('estimation.estimations:form-comments-detail', *args, **kwargs)

