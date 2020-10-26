import uuid

from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.account.models import Country, University, Major
from apps.estimation.estimations.tests.base import EstimationsAppBaseTests
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
        return self._test_form('estimation.estimations:form-comments-detail', *args, **kwargs)

    def test_form_comments_detail_get_200(self):
        self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=uuid.UUID(self.app_form_1.id).hex)

