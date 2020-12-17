from abroadin.apps.estimation.form.tests.apis.form_completion.base import BaseTests as FormCompletionBaseTests


class EndpointMethodMixin:
    def _other_charts(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.analyze:language-other-charts', *args, **kwargs)

    def _endpoint_method(self, *args, **kwargs):
        return self._other_charts(*args, **kwargs)


class OtherChartsFormCompletionTests(EndpointMethodMixin, FormCompletionBaseTests):

    def setUp(self) -> None:
        super().setUp()
