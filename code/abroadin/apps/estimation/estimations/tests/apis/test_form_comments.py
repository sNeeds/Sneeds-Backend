from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.applydata.models import GradeChoices
from abroadin.apps.estimation.form.models import Education
from abroadin.apps.estimation.form.models import WantToApply, StudentDetailedInfo
from abroadin.apps.estimation.tests.base import EstimationTestBase
from abroadin.apps.estimation.form.tests.apis.form_completion.base import FormCompletionBaseTestsMixin

from .test_base import EstimationsAppAPITestBase

User = get_user_model()


class FormCommentsAPITests(EstimationsAppAPITestBase):
    def setUp(self):
        super().setUp()

    def _test_form_comments_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def test_form_comments_detail_get_200(self):
        self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id)


class FormCommentsFormCompletionTests(EstimationsAppAPITestBase, FormCompletionBaseTestsMixin):
    include_in_test = True

    def _form_comments(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def _fc_mixin_endpoint_method(self, *args, **kwargs):
        return self._form_comments(*args, **kwargs)

    def setUp(self) -> None:
        super().setUp()


class FormCommentsUserEmailVerifiedTests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()

    def _form_comments(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def test_user_email_is_verified_get_200(self):
        data = self._form_comments(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_email_is_not_verified_get_403(self):
        self.user1.is_email_verified = False
        self.user1.save()
        data = self._form_comments(
            'get', self.user1, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )


class FormCommentsFormOwnershipTests(EstimationsAppAPITestBase):

    def setUp(self):
        super().setUp()

    def _form_comments(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def test_user_is_owner_get_200(self):
        data = self._form_comments(
            'get', self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id
        )

    def test_user_is_not_owner_get_403(self):
        data = self._form_comments(
            'get', self.user2, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id
        )
