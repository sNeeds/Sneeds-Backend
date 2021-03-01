from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
    Education, WantToApply)

from .test_base import EstimationsAppAPITestBase
from abroadin.apps.estimation.form.tests.apis.form_completion.base import FormCompletionBaseTestsMixin

User = get_user_model()


class WantToApplyChanceAPITests(EstimationsAppAPITestBase):
    def setUp(self):
        super().setUp()

    def _test_want_to_apply_chance(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:want-to-apply-chance', *args, **kwargs)

    def test_want_to_apply_chance_200_1(self):
        self._test_want_to_apply_chance("get", self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id)


class WantToApplyChanceFormCompletionTests(EstimationsAppAPITestBase, FormCompletionBaseTestsMixin):
    include_in_test = True

    def _want_to_apply(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:want-to-apply-chance', *args, **kwargs)

    def _fc_mixin_endpoint_method(self, *args, **kwargs):
        return self._want_to_apply(*args, **kwargs)

    def setUp(self) -> None:
        super().setUp()


class WantToApplyChanceUserEmailVerifiedTests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()

    def _want_to_apply_chances(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:want-to-apply-chance', *args, **kwargs)

    def test_user_email_is_verified_get_200(self):
        data = self._want_to_apply_chances(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_email_is_not_verified_get_403(self):
        self.user1.is_email_verified = False
        self.user1.save()
        data = self._want_to_apply_chances(
            'get', self.user1, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )


class WantToApplyChanceFormOwnershipTests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()

    def _want_to_apply_chances(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:want-to-apply-chance', *args, **kwargs)

    def test_user_is_owner_get_200(self):
        data = self._want_to_apply_chances(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_is_not_owner_get_403(self):
        data = self._want_to_apply_chances(
            'get', self.user2, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )

