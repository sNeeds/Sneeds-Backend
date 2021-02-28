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
        super().setUp()
        self.local_form1 = self.student_detailed_info1

    def _test_form_comments_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.estimations:form-comments', *args, **kwargs)

    def test_publication_get_form_review_200(self):
        for which_author_choice in Publication.WhichAuthorChoices:
            for publication_choice in Publication.PublicationChoices:
                for journal_reputation_choice in Publication.JournalReputationChoices:
                    Publication.objects.create(
                        content_object=self.local_form1,
                        title="Foo title",
                        publish_year=2020,
                        which_author=which_author_choice,
                        type=publication_choice,
                        journal_reputation=journal_reputation_choice
                    )
                    self._test_form_comments_detail("get", self.user1, status.HTTP_200_OK,
                                                    reverse_args=self.local_form1.id)
