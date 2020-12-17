from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear, GradeChoices, \
    UniversityThrough
from abroadin.apps.estimation.form.tests.apis.test_base import FormAPITests

User = get_user_model()


class UniversityThroughAPITest(FormAPITests):

    def setUp(self):
        super().setUp()

        self.local_student_detailed_info = StudentDetailedInfo.objects.create()

        self.university_through_payload = {
            "student_detailed_info": self.local_student_detailed_info.id,
            "university": self.university1.id,
            "grade": GradeChoices.BACHELOR,
            "major": self.major1.id,
            "graduate_in": 2019,
            "thesis_title": "Foo thesis",
            "gpa": 16.5,
        }

        self.local_university_through = UniversityThrough.objects.create(
            student_detailed_info=self.local_student_detailed_info,
            university=self.university1,
            grade=GradeChoices.MASTER,
            major=self.major1,
            graduate_in=2019,
            thesis_title="Foo thesis",
            gpa=17
        )

        self.local_user = User.objects.create_user(email="t1@g.com", password="user1234")

    def _university_through_list(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:university-through-list', *args, **kwargs)

    def _university_through_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:university-through-detail', *args, **kwargs)

    def test_university_through_list_get_200_1(self):
        data = self._university_through_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_university_through_list_get_200_2(self):
        self.local_university_through.student_detailed_info.user = self.local_user
        self.local_university_through.student_detailed_info.save()
        data = self._university_through_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_university_through.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_university_through_list_get_200_3(self):
        self._university_through_list("post", None, status.HTTP_201_CREATED, data=self.university_through_payload)
        data = self._university_through_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.local_university_through.student_detailed_info.id}
        )
        self.assertEqual(len(data), 2)

    def test_university_through_list_get_200_4(self):
        student_detailed_info = StudentDetailedInfo.objects.create(user=self.local_user)
        data = self._university_through_list(
            "get", self.local_user, status.HTTP_200_OK,
            data={"student-detailed-info": student_detailed_info.id}
        )
        self.assertEqual(len(data), 0)

    def test_university_through_list_get_200_5(self):
        student_detailed_info = StudentDetailedInfo.objects.create()
        data = self._university_through_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": student_detailed_info.id}
        )
        self.assertEqual(len(data), 0)

    def test_university_through_list_post_201_1(self):
        self._university_through_list("post", None, status.HTTP_201_CREATED, data=self.university_through_payload)

    def test_university_through_list_post_201_2(self):
        self.local_student_detailed_info.user = self.user1
        self.local_student_detailed_info.save()
        self._university_through_list("post", self.user1, status.HTTP_201_CREATED, data=self.university_through_payload)

    def test_university_through_list_post_400(self):
        self.university_through_payload["grade"] = GradeChoices.MASTER
        self._university_through_list("post", None, status.HTTP_400_BAD_REQUEST, data=self.university_through_payload)

    def test_university_through_detail_get_200_1(self):
        self._university_through_detail("get", None, status.HTTP_200_OK, reverse_args=self.local_university_through.id)

    def test_university_through_detail_get_200_2(self):
        self.local_university_through.student_detailed_info.user = self.user1
        self.local_university_through.student_detailed_info.save()
        self._university_through_detail(
            "get", self.user1, status.HTTP_200_OK, reverse_args=self.local_university_through.id
        )

    def test_university_through_detail_delete_200_1(self):
        self._university_through_detail(
            "delete", None, status.HTTP_204_NO_CONTENT, reverse_args=self.local_university_through.id
        )
        self.assertEqual(UniversityThrough.objects.filter(id=self.local_university_through.id).count(), 0)

    def test_university_through_detail_delete_200_2(self):
        self.local_university_through.student_detailed_info.user = self.user1
        self.local_university_through.student_detailed_info.save()
        self._university_through_detail(
            "delete", self.user1, status.HTTP_204_NO_CONTENT, reverse_args=self.local_university_through.id
        )
        self.assertEqual(UniversityThrough.objects.filter(id=self.local_university_through.id).count(), 0)
