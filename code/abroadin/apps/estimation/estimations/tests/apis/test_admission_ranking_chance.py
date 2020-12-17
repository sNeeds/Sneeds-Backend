from django.contrib.auth import get_user_model

from rest_framework import status

from .test_base import EstimationsAppAPITests
from abroadin.apps.estimation.form.tests.apis.form_completion.base import BaseTests as FormCompletionBaseTests

from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
)

User = get_user_model()


class AdmissionRankingChanceAPITests(EstimationsAppAPITests):
    def setUp(self):
        super().setUp()

    def _test_admission_ranking_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-admission-ranking-chance', *args, **kwargs)

    def test_admission_ranking_chance_200_1(self):
        self._test_admission_ranking_chance("get", None, status.HTTP_200_OK, reverse_args=self.app_form_1.id)

    def test_admission_ranking_chance_200_2(self):
        form = StudentDetailedInfo.objects.create()
        self._test_admission_ranking_chance("get", None, status.HTTP_200_OK, reverse_args=form.id)


class EndpointMethodMixin:
    def _admission_ranking_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-admission-ranking-chance', *args, **kwargs)

    def _endpoint_method(self, *args, **kwargs):
        return self._admission_ranking_chance(*args, **kwargs)


class AdmissionRankingChanceFormCompletionTests(EndpointMethodMixin, FormCompletionBaseTests):
    include_in_test = True

    def setUp(self) -> None:
        super().setUp()
