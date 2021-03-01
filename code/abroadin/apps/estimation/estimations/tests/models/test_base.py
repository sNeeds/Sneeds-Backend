from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.estimations.tests.test_base import EstimationsAppTestsBase


User = get_user_model()


class EstimationsAppModelTestBase(EstimationsAppTestsBase):

    def setUp(self):
        super().setUp()
