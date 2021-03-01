from django.contrib.auth import get_user_model

from .test_base import EstimationsAppModelTestBase

User = get_user_model()


class StudentDetailedInfoModelTests(EstimationsAppModelTestBase):

    def setUp(self):
        super().setUp()

