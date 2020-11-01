from django.contrib.auth import get_user_model

from rest_framework import status

from .test_base import SimilarApplyAppAPITests
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


class SimilarUniversitiesAPITests(SimilarApplyAppAPITests):
    def setUp(self):
        super().setUp()

    def test_similar_universities_200_1(self):
        self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)

    def test_similar_universities_200_2(self):
        form = StudentDetailedInfo.objects.create()
        self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=form.id)
