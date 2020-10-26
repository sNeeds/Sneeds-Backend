from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear
from abroadin.apps.data.account.models import Country, University, Major

User = get_user_model()


class FormAPITests(EstimationBaseTest):

    def setUp(self):
        super().setUp()
