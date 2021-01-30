from abroadin.apps.data.account.models import Country
from ..base import SimilarProfilesBaseTests
from ...functions import get_preferred_apply_country


class SimilarProfilesFunctionsBaseTests(SimilarProfilesBaseTests):
    def setUp(self):
        super().setUp()

    def test_get_preferred_apply_country(self):
        canada, _ = Country.objects.get_or_create(name="Canada", search_name="canada", slug="canada")
        self.assertEqual(get_preferred_apply_country(), canada)