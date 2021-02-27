from django.contrib.auth import get_user_model

from ..test_base import EstimationsAppTestsBase

User = get_user_model()


class EstimationsAppAPITestBase(EstimationsAppTestsBase):

    def setUp(self):
        super().setUp()
