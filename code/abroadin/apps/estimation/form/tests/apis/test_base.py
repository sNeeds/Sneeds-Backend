from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.applydata.models import GradeChoices
from abroadin.apps.estimation.tests.base import EstimationTestBase
from abroadin.apps.estimation.form.models import StudentDetailedInfo

User = get_user_model()


class FormAPITestBase(EstimationTestBase):

    def setUp(self):
        super().setUp()

        self.payload = {
            "age": 22,
            "gender": "Male",
            "is_married": None,
            "resume": None,
            "related_work_experience": 22,
            "academic_break": 19,
            "olympiad": None,
            "want_to_apply": {
                "countries": [self.country1.id, self.country2.id],
                "universities": [self.university1.id, self.university2.id],
                "grades": [self.master_grade, self.phd_grade],
                "majors": [self.major1, self.major2],
                "semester_years": [16]
            },
            "educations": [
                {
                    "graduate_in": 2020,
                    "thesis_title": None,
                    "major": self.major3,
                    "grade": GradeChoices.BACHELOR,
                    "university": self.university2,
                    "gpa": "19.00"
                },
                {
                    "graduate_in": 2018,
                    "thesis_title": "Be to che",
                    "major": self.major4,
                    "grade": GradeChoices.MASTER,
                    "university": self.university5,
                    "gpa": "18.00"
                }
            ],
            "publications": [
                {
                    "journal_reputation": "Four to ten",
                    "publish_year": 2020,
                    "which_author": "Second",
                    "type": "Journal",
                    "title": "sdfsdf"
                },
                {
                    "journal_reputation": "Four to ten",
                    "publish_year": 2018,
                    "which_author": "Fourth or more",
                    "type": "Journal",
                    "title": "ffff"
                }
            ],
            "language_certificates": [
                {
                    "is_mock": false,
                    "certificate_type": "TOEFL"
                },
                {
                    "is_mock": true,
                    "certificate_type": "IELTS General"
                }
            ],
            "payment_affordability": None,
            "prefers_full_fund": None,
            "prefers_half_fund": None,
            "prefers_self_fund": None,
            "comment": "",
            "powerful_recommendation": false,
            "linkedin_url": None,
            "homepage_url": None
        }

    def _test_form_list(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:student-detailed-info-list', *args, **kwargs)

    def _test_form_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:student-detailed-info-detail', *args, **kwargs)

    def test_form_list_post_201(self):
        self._test_form_list("post", None, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED, data={"age": 20}, )
        self._test_form_list("post", None, status.HTTP_201_CREATED)

    def test_form_list_post_403(self):
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_403_FORBIDDEN)

    def test_form_detail_get_200(self):
        data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=data['id'])
        self._test_form_detail("get", None, status.HTTP_200_OK, reverse_args=data['id'])

    def test_form_detail_put_patch_200(self):
        def _update_all_fields(update_method, update_fields):
            data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
            for k, v in update_fields.items():
                data = self._test_form_detail(
                    update_method, self.user1, status.HTTP_200_OK, reverse_args=data['id'], data={k: v},
                )

            obj = StudentDetailedInfo.objects.get(id=data['id'])
            for k in update_fields.keys():
                self.assertEqual(getattr(obj, k), data[k])
                self.assertEqual(getattr(obj, k), update_fields[k])
            obj.delete()

        all_update_fields = {
            "age": 20,
            "related_work_experience": 5,
            "academic_break": 5,
            "olympiad": "Foo olympiad",
            "gender": "Male",
            "payment_affordability": "High",
            "prefers_full_fund": True,
            "prefers_half_fund": False,
            "prefers_self_fund": True,
            "comment": "Foo comment",
            "powerful_recommendation": True,
            "linkedin_url": "https://www.linkedin.com/in/foo/",
            "homepage_url": "https://www.foo.com/",
        }

        _update_all_fields("put", all_update_fields)
        _update_all_fields("patch", all_update_fields)

        obj = StudentDetailedInfo.objects.create()
        self._test_form_detail("put", self.user2, status.HTTP_200_OK, reverse_args=obj.id)
        obj.delete()

        obj = StudentDetailedInfo.objects.create()
        self._test_form_detail("patch", self.user2, status.HTTP_200_OK, reverse_args=obj.id)
        obj.delete()

        obj = StudentDetailedInfo.objects.create()
        self._test_form_detail("put", None, status.HTTP_200_OK, reverse_args=obj.id)
        self._test_form_detail("patch", None, status.HTTP_200_OK, reverse_args=obj.id)
        obj.delete()

    def test_form_detail_get_403(self):
        data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=data['id'])
        self._test_form_detail("get", None, status.HTTP_401_UNAUTHORIZED, reverse_args=data['id'])
        self._test_form_detail("get", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=data['id'])

    def test_form_detail_put_patch_403(self):
        data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_detail("put", None, status.HTTP_401_UNAUTHORIZED, reverse_args=data['id'])
        self._test_form_detail("patch", None, status.HTTP_401_UNAUTHORIZED, reverse_args=data['id'])
        self._test_form_detail("put", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=data['id'])
        self._test_form_detail("patch", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=data['id'])
