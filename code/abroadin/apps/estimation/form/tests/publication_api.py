from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, Publication, SemesterYear
from abroadin.apps.data.account.models import Country, University, Major
from abroadin.apps.estimation.form.tests.apis import FormAPITests

User = get_user_model()


class PublicationAPITest(FormAPITests):

    def setUp(self):
        super().setUp()

        self.student_detailed_info = StudentDetailedInfo.objects.create()

        self.publication_payload = {
            "student_detailed_info": self.student_detailed_info.id,
            'title': 'sample title 2',
            'publish_year': 2016,
            'which_author': Publication.WhichAuthorChoices.SECOND,
            'type': Publication.PublicationChoices.JOURNAL,
            'journal_reputation': Publication.JournalReputationChoices.ONE_TO_THREE,
        }

        self.local_student_detailed_info = StudentDetailedInfo.objects.create()
        self.local_publication = Publication.objects.create(student_detailed_info=self.local_student_detailed_info,
                                                            which_author=Publication.WhichAuthorChoices.FIRST,
                                                            title='sample title 1',
                                                            type=Publication.PublicationChoices.CONFERENCE,
                                                            publish_year=2018,
                                                            journal_reputation=Publication.JournalReputationChoices.
                                                            FOUR_TO_TEN,
                                                            )

        self.local_user = User.objects.create_user(email="t1@g.com", password="user1234")

    def _publication_list(self, *args, **kwargs):
        return self._test_form('estimation.form:publication-list', *args, **kwargs)

    def _publication_detail(self, *args, **kwargs):
        return self._test_form('estimation.form:publication-detail', *args, **kwargs)

    def test_university_through_list_get_200_1(self):
        data = self._publication_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_university_through_list_get_200_2(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_publication.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_university_through_list_get_200_3(self):
        sdi = StudentDetailedInfo.objects.create(user=self.local_user)
        data = self._publication_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": sdi.id}
        )
        self.assertEqual(len(data), 0)

    def test_university_through_list_get_200_4(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_publication.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_university_through_list_post_201_1(self):
        data = self._publication_list(
            "post", None, status.HTTP_201_CREATED,
            data=self.publication_payload
        )
        data = self._publication_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.publication_payload.get('student_detailed_info')}
        )
        self.assertEqual(len(data), 1)
