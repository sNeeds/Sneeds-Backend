from django.contrib.auth import get_user_model

from ..test_base import EstimationsAppBaseTests

User = get_user_model()


class EstimationsAppAPITests(EstimationsAppBaseTests):

    def setUp(self):
        super().setUp()

    def _test_form_comments_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)
