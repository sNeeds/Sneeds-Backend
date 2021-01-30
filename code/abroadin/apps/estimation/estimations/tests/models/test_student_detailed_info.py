from django.contrib.auth import get_user_model

from rest_framework import status

from .test_base import EstimationsAppModelTests
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


class StudentDetailedInfoModelTests(EstimationsAppModelTests):

    def setUp(self):
        super().setUp()

