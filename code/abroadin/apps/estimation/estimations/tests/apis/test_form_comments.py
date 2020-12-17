from django.contrib.auth import get_user_model

from rest_framework import status

from .test_base import EstimationsAppAPITests
from abroadin.apps.estimation.form.tests.apis.form_completion.base import BaseTests as FormCompletionBaseTests

User = get_user_model()


class FormCommentsAPITests(EstimationsAppAPITests):
    def setUp(self):
        super().setUp()

    def test_form_comments_detail_get_200(self):
        self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)


class EndpointMethodMixin:
    def _form_comments(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def _endpoint_method(self, *args, **kwargs):
        return self._form_comments(*args, **kwargs)


class FormCommentsAPITestsFormCompletionTests(EndpointMethodMixin, FormCompletionBaseTests):

    def setUp(self) -> None:
        super().setUp()