from django.contrib.auth import get_user_model

from rest_framework import status

from ..test_base import SimilarApplyAppBaseTests
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


class SimilarApplyAppAPITests(SimilarApplyAppBaseTests):

    def setUp(self):
        super().setUp()

    def _test_similar_universities(self, *args, **kwargs):
        return self._endpoint_test_method('similar_apply:similar-universities', *args, **kwargs)
