from django.contrib.auth import get_user_model

from rest_framework import status

from ..test_base import EstimationsAppBaseTests
from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
    Grade,
    WantToApply,
    SemesterYear,
    UniversityThrough,
    GradeChoices,
    Publication,
    RegularLanguageCertificate,
    LanguageCertificate
)

User = get_user_model()


class EstimationsAppAPITests(EstimationsAppBaseTests):

    def setUp(self):
        super().setUp()

    def _test_form_comments_detail(self, *args, **kwargs):
        return self._test_form('estimation.estimations:form-comments', *args, **kwargs)
