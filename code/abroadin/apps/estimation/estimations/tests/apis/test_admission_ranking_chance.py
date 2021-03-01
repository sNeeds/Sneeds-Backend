from django.contrib.auth import get_user_model

from rest_framework import status

from .test_base import EstimationsAppAPITestBase
from abroadin.apps.estimation.form.tests.apis.form_completion.base import FormCompletionBaseTestsMixin


User = get_user_model()


class AdmissionRankingChanceAPITests(EstimationsAppAPITestBase):
    def setUp(self):
        super().setUp()

    def _test_admission_ranking_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-admission-ranking-chance', *args, **kwargs)

    def test_admission_ranking_chance_200_1(self):
        self._test_admission_ranking_chance("get", self.user1, status.HTTP_200_OK,
                                            reverse_args=self.student_detailed_info1.id)


class AdmissionRankingChanceFormCompletionTests(EstimationsAppAPITestBase, FormCompletionBaseTestsMixin):
    include_in_test = True

    def _admission_ranking_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-admission-ranking-chance', *args, **kwargs)

    def _fc_mixin_endpoint_method(self, *args, **kwargs):
        return self._admission_ranking_chance(*args, **kwargs)

    def setUp(self) -> None:
        super().setUp()


class AdmissionRankingChanceUserEmailVerifiedTests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()

    def _admission_ranking_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-admission-ranking-chance', *args, **kwargs)

    def test_user_email_is_verified_get_200(self):
        data = self._admission_ranking_chance(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_email_is_not_verified_get_403(self):
        self.user1.is_email_verified = False
        self.user1.save()
        data = self._admission_ranking_chance(
            'get', self.user1, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )


class AdmissionRankingChanceFormOwnershipTests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()

    def _admission_ranking_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-admission-ranking-chance', *args, **kwargs)

    def test_user_is_owner_get_200(self):
        data = self._admission_ranking_chance(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_is_not_owner_get_403(self):
        data = self._admission_ranking_chance(
            'get', self.user2, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )
