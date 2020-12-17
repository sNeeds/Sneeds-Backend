from abroadin.apps.estimation.form.tests.apis.form_completion.base import BaseTests as FormCompletionBaseTests


class EndpointMethodMixin:
    def _language_certificates_charts(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.analyze:language-certificates-charts', *args, **kwargs)

    def _endpoint_method(self, *args, **kwargs):
        return self._language_certificates_charts(*args, **kwargs)


class LanguageCertificatesChartsFormCompletionTests(EndpointMethodMixin, FormCompletionBaseTests):

    def setUp(self) -> None:
        super().setUp()
