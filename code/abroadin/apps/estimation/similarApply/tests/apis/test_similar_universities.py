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
from abroadin.apps.estimation.form.tests.apis.form_completion.base import BaseTests as FormCompletionBaseTests

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
            student_detailed_info=self.app_applied_student_form_1,
            certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL,
            listening=90,
            speaking=90,
            writing=90,
            reading=90,
            overall=90
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(data[0]['language_certificate'], "TOEFL 90.0")

        RegularLanguageCertificate.objects.create(
            student_detailed_info=self.app_applied_student_form_1,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            listening=8,
            speaking=8,
            writing=8,
            reading=8,
            overall=8
        )
        data = self._test_similar_universities("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)
        self.assertEqual(data[0]['language_certificate'], "TOEFL 90.0 & IELTS General 8.0")


class EndpointMethodMixin:
    def _similar_universities(self, *args, **kwargs):
        return self._endpoint_test_method('similar_apply:similar-universities', *args, **kwargs)

    def _endpoint_method(self, *args, **kwargs):
        return self._similar_universities(*args, **kwargs)


class SimilarUniversitiesFormCompletionTests(EndpointMethodMixin, FormCompletionBaseTests):
    include_in_test = True

    def setUp(self) -> None:
        super().setUp()
