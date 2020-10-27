import uuid

from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.account.models import Country, University, Major
from apps.estimation.estimations.tests.apis.base import EstimationsAppAPITests
from apps.estimation.estimations.tests.models.base import EstimationsAppModelTests
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


class LanguageCertificateModelTests(EstimationsAppAPITests):

    def setUp(self):
        self.local_form1 = StudentDetailedInfo.objects.create()
        super().setUp()

    def test_language_certificate_form_review_200(self):
        RegularLanguageCertificate.objects.create(
            student_detailed_info=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL,
            speaking=90,
            listening=90,
            reading=90,
            writing=90,
            overall=90
        )
        self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)

        RegularLanguageCertificate.objects.create(
            student_detailed_info=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
            speaking=7,
            listening=6,
            reading=7,
            writing=7,
            overall=7
        )
        self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)

        RegularLanguageCertificate.objects.create(
            student_detailed_info=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            speaking=7,
            listening=7,
            reading=7,
            writing=7,
            overall=7
        )
        data = self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)

        print(data["language"])