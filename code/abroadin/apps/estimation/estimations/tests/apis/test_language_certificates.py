from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework import status

from abroadin.apps.data.applydata.models import DuolingoCertificate, RegularLanguageCertificate, GREGeneralCertificate
from .test_base import EstimationsAppAPITestBase
from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
    Grade,
    WantToApply,
    SemesterYear,
    Education,
    Publication,
    LanguageCertificate
)

User = get_user_model()


class LanguageCertificateAPITests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()
        self.local_form1 = self.student_detailed_info2

    def _test_form_comments_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def test_language_certificate_form_review_200(self):
        def _test_total_value():
            data = self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)
            max_value = 0
            for certificate in LanguageCertificate.objects.filter(
                    content_type=ContentType.objects.get_for_model(self.local_form1.__class__),
                    object_id=self.local_form1.id):

                if certificate.value:
                    max_value = max(certificate.value, max_value)
            self.assertEqual(data['language']['total_value'], max_value)

        DuolingoCertificate.objects.create(
            content_object=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.DUOLINGO,
            literacy=90,
            comprehension=90,
            conversation=90,
            production=90,
            overall=90
        )
        _test_total_value()

        RegularLanguageCertificate.objects.filter(
            content_type=ContentType.objects.get_for_model(self.local_form1.__class__),
            object_id=self.local_form1.id,
            certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL).delete()

        RegularLanguageCertificate.objects.create(
            content_object=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.TOEFL,
            speaking=90,
            listening=90,
            reading=90,
            writing=90,
            overall=90
        )
        _test_total_value()

        RegularLanguageCertificate.objects.filter(
            content_type=ContentType.objects.get_for_model(self.local_form1.__class__),
            object_id=self.local_form1.id,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC).delete()

        RegularLanguageCertificate.objects.create(
            content_object=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_ACADEMIC,
            speaking=7,
            listening=6,
            reading=7,
            writing=7,
            overall=7
        )
        _test_total_value()

        RegularLanguageCertificate.objects.filter(
            content_type=ContentType.objects.get_for_model(self.local_form1.__class__),
            object_id=self.local_form1.id,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL).delete()

        RegularLanguageCertificate.objects.create(
            content_object=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.IELTS_GENERAL,
            speaking=7,
            listening=7,
            reading=7,
            writing=7,
            overall=7
        )
        _test_total_value()

        RegularLanguageCertificate.objects.filter(
            content_type=ContentType.objects.get_for_model(self.local_form1.__class__),
            object_id=self.local_form1.id,
            certificate_type=LanguageCertificate.LanguageCertificateType.GRE_GENERAL).delete()

        GREGeneralCertificate.objects.create(
            content_object=self.local_form1,
            certificate_type=LanguageCertificate.LanguageCertificateType.GRE_GENERAL,
            quantitative=150,
            verbal=140,
            analytical_writing=3.2
        )
        _test_total_value()
