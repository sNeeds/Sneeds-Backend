from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.similarApply.models import AppliedTo
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

from .test_base import SimilarApplyAppAPITests

User = get_user_model()


class SimilarUniversitiesAPITests(SimilarApplyAppAPITests):
    def setUp(self):
        super().setUp()

    def test_similar_universities_200_1(self):
        self.create_applied_to()
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['applied_university']['id'], self.university3.id)

    def test_similar_universities_200_2(self):
        self.app_applied_student_form_1_applied_to_1.delete()
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 0)

    def test_similar_universities_200_3(self):
        self.app_applied_student_form_1_applied_to_1.delete()
        AppliedTo.objects.create(
            applied_student_detailed_info=self.app_applied_student_form_1,
            university=self.university2,
            grade=GradeChoices.PHD,
            major=self.major1,
            semester_year=self.semester_year2,
            fund=20000,
            accepted=True,
            comment="Foo comment"
        )

        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 0)
