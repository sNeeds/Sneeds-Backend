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
        self.create_applied_to(
            self.app_applied_student_form_1, self.university1,
            grade=GradeChoices.PHD, major=self.major3
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['applied_university']['id'], self.university1.id)

    def test_similar_universities_200_2(self):
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 0)

    def test_similar_universities_200_3(self):
        self.create_applied_to(
            self.app_applied_student_form_1, self.university3,
            grade=GradeChoices.PHD, major=self.major3
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 0)

    def test_similar_universities_200_4(self):
        self.create_applied_to(
            self.app_applied_student_form_1, self.university1,
            grade=GradeChoices.BACHELOR, major=self.major3
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(len(data), 0)

    def test_similar_universities_200_5(self):
        self.create_applied_to(
            self.app_applied_student_form_1, self.university1,
            grade=GradeChoices.PHD, major=self.major3
        )

        RegularLanguageCertificate.objects.create(
            student_detailed_info = self.app_applied_student_form_1,
            certificate_type = LanguageCertificate.LanguageCertificateType.TOEFL,
            listening=90,
            speaking=90,
            writing=90,
            reading=90,
            overall=90
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        print(data)
        RegularLanguageCertificate.objects.create(
            student_detailed_info = self.app_applied_student_form_1,
            certificate_type = LanguageCertificate.LanguageCertificateType.TOEFL,
            listening=90,
            speaking=90,
            writing=90,
            reading=90,
            overall=90
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        print(data)