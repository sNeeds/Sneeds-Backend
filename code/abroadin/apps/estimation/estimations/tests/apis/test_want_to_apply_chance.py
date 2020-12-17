from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
)

from .test_base import EstimationsAppAPITests
from abroadin.apps.estimation.form.tests.apis.form_completion.base import BaseTests as FormCompletionBaseTests

User = get_user_model()


class WantToApplyChanceAPITests(EstimationsAppAPITests):
    def setUp(self):
        super().setUp()

    def _test_want_to_apply_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:want-to-apply-chance', *args, **kwargs)

    def test_want_to_apply_chance_200_1(self):
        self._test_want_to_apply_chance("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)

    def test_want_to_apply_chance_200_2(self):
        form = StudentDetailedInfo.objects.create()
        self._test_want_to_apply_chance("get", None, status.HTTP_200_OK, reverse_args=form.id)


class EndpointMethodMixin:
    def _want_to_apply(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:want-to-apply-chance', *args, **kwargs)

    def _endpoint_method(self, *args, **kwargs):
        return self._want_to_apply(*args, **kwargs)


class WantToApplyChanceFormCompletionTests(EndpointMethodMixin, FormCompletionBaseTests):
    include_in_test = True

    def setUp(self) -> None:
        super().setUp()
