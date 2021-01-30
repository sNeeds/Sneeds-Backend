from django.contrib.auth import get_user_model

from ..base import SimilarProfilesBaseTests

User = get_user_model()


class SimilarProfilesFunctionsBaseTests(SimilarProfilesBaseTests):
    def setUp(self):
        super().setUp()

