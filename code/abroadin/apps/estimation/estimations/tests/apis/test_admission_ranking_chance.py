from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.estimations.tests.apis.test_base import EstimationsAppAPITests
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


class FormCommentsAPITests(EstimationsAppAPITests):
    def setUp(self):
        super().setUp()

    def _test_admission_ranking_chance(self, *args, **kwargs):
        return self._test_form('estimation.estimations:form-comments', *args, **kwargs)

    def test_admission_ranking_chance_200(self):
        self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
