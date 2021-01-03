from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.estimations.tests.test_base import EstimationsAppBaseTests
from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
    Grade,
    WantToApply,
    SemesterYear,
    Education,
    GradeChoices,
    Publication,
    RegularLanguageCertificate,
    LanguageCertificate
)

User = get_user_model()


class EstimationsAppModelTests(EstimationsAppBaseTests):

    def setUp(self):
        super().setUp()

