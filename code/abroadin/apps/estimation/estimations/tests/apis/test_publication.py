from django.contrib.auth import get_user_model

from rest_framework import status

from .test_base import EstimationsAppAPITestBase
from abroadin.apps.estimation.form.models import (
    StudentDetailedInfo,
    Publication,
)

User = get_user_model()


class PublicationAPITests(EstimationsAppAPITestBase):

    def setUp(self):
        self.local_form1 = StudentDetailedInfo.objects.create()
        super().setUp()

    def test_publication_get_form_review_200(self):
        for which_author_choice in Publication.WhichAuthorChoices:
            for publication_choice in Publication.PublicationChoices:
                for journal_reputation_choice in Publication.JournalReputationChoices:
                    Publication.objects.create(
                        student_detailed_info=self.local_form1,
                        title="Foo title",
                        publish_year=2020,
                        which_author=which_author_choice,
                        type=publication_choice,
                        journal_reputation=journal_reputation_choice
                    )
                    self._test_form_comments_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_form1.id)
