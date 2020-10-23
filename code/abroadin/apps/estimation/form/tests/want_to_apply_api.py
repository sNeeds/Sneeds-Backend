from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear
from abroadin.apps.data.account.models import Country, University, Major
from abroadin.apps.estimation.form.tests.apis import FormAPITests

User = get_user_model()


class WantToApplyAPITest(FormAPITests):

    def setUp(self):
        super().setUp()

        self.student_detailed_info = StudentDetailedInfo.objects.create()

        self.want_to_apply_payload = {
            "student_detailed_info": self.student_detailed_info.id,
            "countries": [country.id for country in Country.objects.all()][:-1],
            "grades": [grade.id for grade in Grade.objects.all()][:-1],
            "universities": [university.id for university in University.objects.all()][:-1],
            "majors": [major.id for major in Major.objects.all()][:-1],
            "semester_years": [semester.id for semester in SemesterYear.objects.all()][:-1]
        }

        temp_student_detailed_info = StudentDetailedInfo.objects.create()
        self.want_to_apply1 = WantToApply.objects.create(student_detailed_info=temp_student_detailed_info)
        self.want_to_apply1.countries.set(Country.objects.all())
        self.want_to_apply1.universities.set(University.objects.all())
        self.want_to_apply1.grades.set(Grade.objects.all())
        self.want_to_apply1.majors.set(Major.objects.all())
        self.want_to_apply1.semester_years.set(SemesterYear.objects.all())

        self.temp_user = User.objects.create_user(email="t1@g.com", password="user1234")

    def _want_to_apply_list(self, *args, **kwargs):
        return self._test_form('estimation.form:want-to-apply-list', *args, **kwargs)

    def _want_to_apply_detail(self, *args, **kwargs):
        return self._test_form('estimation.form:want-to-apply-detail', *args, **kwargs)

    def test_want_to_apply_list_get_200_1(self):
        data = self._want_to_apply_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": self.want_to_apply1.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_want_to_apply_list_get_200_2(self):
        self.want_to_apply1.student_detailed_info.user = self.temp_user
        self.want_to_apply1.student_detailed_info.save()
        data = self._want_to_apply_list(
            "get", self.temp_user, status.HTTP_200_OK,
            data={"student-detailed-info": self.want_to_apply1.student_detailed_info.id}
        )
        self.assertEqual(len(data), 1)

    def test_want_to_apply_list_get_200_3(self):
        student_detailed_info = StudentDetailedInfo.objects.create(user=self.temp_user)
        data = self._want_to_apply_list(
            "get", self.temp_user, status.HTTP_200_OK,
            data={"student-detailed-info": student_detailed_info.id}
        )
        self.assertEqual(len(data), 0)

    def test_want_to_apply_list_get_200(self):
        student_detailed_info = StudentDetailedInfo.objects.create()
        data = self._want_to_apply_list(
            "get", None, status.HTTP_200_OK,
            data={"student-detailed-info": student_detailed_info.id}
        )
        self.assertEqual(len(data), 0)

    def test_want_to_apply_list_post_201_1(self):
        payload = {k: v for k, v in self.want_to_apply_payload.items() if
                   k in ["student_detailed_info", "countries", "grades"]}
        self._want_to_apply_list("post", None, status.HTTP_201_CREATED, data=payload)

    def test_want_to_apply_list_post_201_2(self):
        payload = self.want_to_apply_payload
        data = self._want_to_apply_list("post", None, status.HTTP_201_CREATED, data=payload)
        want_to_apply = WantToApply.objects.get(id=data['id'])

        self.assertEqual(want_to_apply.student_detailed_info.id, data["student_detailed_info"])
        self.assertEqual([c.id for c in want_to_apply.countries.all()], payload['countries'])
        self.assertEqual([u.id for u in want_to_apply.universities.all()], payload['universities'])
        self.assertEqual([g.id for g in want_to_apply.grades.all()], payload['grades'])
        self.assertEqual([m.id for m in want_to_apply.majors.all()], payload['majors'])
        self.assertEqual([s.id for s in want_to_apply.semester_years.all()], payload['semester_years'])

    def test_want_to_apply_list_post_201_3(self):
        payload = self.want_to_apply_payload
        self.student_detailed_info.user = self.user1
        self.student_detailed_info.save()
        self._want_to_apply_list("post", self.user1, status.HTTP_201_CREATED, data=payload)

    def test_want_to_apply_list_post_400(self):
        form, _ = StudentDetailedInfo.objects.get_or_create(user=self.user1)
        payload = {
            "student_detailed_info": form.id,
            "countries": [country.id for country in Country.objects.all()][:-1],
            "grades": [grade.id for grade in Grade.objects.all()][:-1],
        }
        data = self._want_to_apply_list("post", self.user1, status.HTTP_201_CREATED, data=payload)
        WantToApply.objects.get(id=data['id']).delete()

        self._want_to_apply_list(
            "post", self.user1, status.HTTP_400_BAD_REQUEST, data={k: v for k, v in payload.items() if k != "countries"}
        )
        self._want_to_apply_list(
            "post", self.user1, status.HTTP_400_BAD_REQUEST, data={k: v for k, v in payload.items() if k != "grades"}
        )

    def test_want_to_apply_detail_get_200_1(self):
        obj = self.want_to_apply1
        data = self._want_to_apply_detail("get", None, status.HTTP_200_OK, reverse_args=obj.id)
        self.assertEqual(data["id"], obj.id)

    def test_want_to_apply_detail_get_200_2(self):
        obj = self.want_to_apply1
        obj.student_detailed_info.user = self.temp_user
        obj.student_detailed_info.save()
        data = self._want_to_apply_detail("get", self.temp_user, status.HTTP_200_OK, reverse_args=obj.id)
        self.assertEqual(data["id"], obj.id)
