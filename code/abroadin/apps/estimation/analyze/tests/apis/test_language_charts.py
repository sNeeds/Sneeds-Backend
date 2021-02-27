from rest_framework import status

from abroadin.apps.estimation.analyze.tests.apis.base import AnalyzeAPITestBase
from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.estimation.form.tests.apis.form_completion.base import FormCompletionBaseTestsMixin
from abroadin.apps.estimation.tests.base import EstimationTestBase


class LanguageCertificatesChartsFormCompletionTests(AnalyzeAPITestBase,
                                                    FormCompletionBaseTestsMixin):
    include_in_test = True

    def _language_certificates_charts(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.analyze:language-certificates-charts', *args, **kwargs)

    def _fc_mixin_endpoint_method(self, *args, **kwargs):
        return self._language_certificates_charts(*args, **kwargs)

    def setUp(self) -> None:
        super().setUp()


class LanguageCertificatesChartsUserEmailVerifiedTests(AnalyzeAPITestBase):

    def setUp(self):
        super().setUp()

    def _language_certificates_charts(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.analyze:language-certificates-charts', *args, **kwargs)

    def test_user_email_is_verified_get_200(self):
        data = self._language_certificates_charts(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_email_is_not_verified_get_403(self):
        self.user1.is_email_verified = False
        self.user1.save()
        data = self._language_certificates_charts(
            'get', self.user1, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )
