from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.estimation.form.models import StudentDetailedInfo, Publication
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
        self.local_publication = Publication.objects.create(
            student_detailed_info=self.local_student_detailed_info,
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

    def test_publication_list_get_200_1(self):
        data = self._publication_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_publication_list_get_200_2(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_publication.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_publication_list_get_200_3(self):
        sdi = StudentDetailedInfo.objects.create(user=self.local_user)
        data = self._publication_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": sdi.id}
        )
        self.assertEqual(len(data), 0)

    def test_publication_list_get_200_4(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_publication.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_publication_list_post_201_1(self):
        data = self._publication_list(
            "post", None, status.HTTP_201_CREATED,
            data=self.publication_payload
        )
        data = self._publication_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.publication_payload.get('student_detailed_info')}
        )
        self.assertEqual(len(data), 1)

    def test_publication_list_post_201_2(self):
        self.student_detailed_info.user = self.local_user
        self.student_detailed_info.save()
        data = self._publication_list(
            "post", self.local_user, status.HTTP_201_CREATED,
            data=self.publication_payload
        )
        data = self._publication_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": self.publication_payload.get('student_detailed_info')}
        )
        self.assertEqual(len(data), 1)

    def test_publication_list_post_400_1(self):
        self.student_detailed_info.user = self.user1
        self.student_detailed_info.save()
        data = self._publication_list(
            "post", self.local_user, status.HTTP_400_BAD_REQUEST,
            data=self.publication_payload
        )
        data = self._publication_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": self.publication_payload.get('student_detailed_info')}
        )
        self.assertEqual(len(data), 0)

    def test_publication_list_post_400_2(self):
        data = self._publication_list(
            "post", self.local_user, status.HTTP_400_BAD_REQUEST,
            data=self.publication_payload
        )

    def test_publication_detail_get_200_1(self):
        data = self._publication_detail(
            "get", None, status.HTTP_200_OK, reverse_args=self.local_publication.id
        )
        self.assertEqual(len(data), 7)

    def test_publication_detail_get_200_2(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "get", self.local_user, status.HTTP_200_OK, reverse_args=self.local_publication.id
        )
        self.assertEqual(len(data), 7)

    def test_publication_detail_get_403_1(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "get", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.local_publication.id
        )

    def test_publication_detail_get_403_2(self):
        data = self._publication_detail(
            "get", self.local_user, status.HTTP_403_FORBIDDEN, reverse_args=self.local_publication.id
        )

    def test_publication_detail_put_405_1(self):
        data = self._publication_detail(
            "put", None, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_put_405_2(self):
        data = self._publication_detail(
            "put", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_put_405_3(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "put", None, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_put_405_4(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "put", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_patch_405_1(self):
        data = self._publication_detail(
            "patch", None, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_patch_405_2(self):
        data = self._publication_detail(
            "patch", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_patch_405_3(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "patch", None, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_patch_405_4(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "patch", self.local_user, status.HTTP_405_METHOD_NOT_ALLOWED, reverse_args=self.local_publication.id,
            data=self.publication_payload,
        )

    def test_publication_detail_delete_204_1(self):
        data = self._publication_detail(
            "delete", None, status.HTTP_204_NO_CONTENT, reverse_args=self.local_publication.id
        )
        self.assertEqual(Publication.objects.filter(id=self.local_publication.id).count(), 0)

    def test_publication_detail_delete_204_2(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "delete", self.local_user, status.HTTP_204_NO_CONTENT, reverse_args=self.local_publication.id
        )
        self.assertEqual(Publication.objects.filter(id=self.local_publication.id).count(), 0)

    def test_publication_detail_delete_401_1(self):
        self.local_publication.student_detailed_info.user = self.local_user
        self.local_publication.student_detailed_info.save()
        data = self._publication_detail(
            "delete", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.local_publication.id
        )

    def test_publication_detail_delete_403_1(self):
        data = self._publication_detail(
            "delete", self.local_user, status.HTTP_403_FORBIDDEN, reverse_args=self.local_publication.id
        )
