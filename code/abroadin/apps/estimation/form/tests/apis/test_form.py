from django.contrib.auth import get_user_model

from rest_framework import status

from abroadin.apps.data.applydata.models import GradeChoices, LanguageCertificate, Publication

from abroadin.apps.estimation.form.tests.apis.test_base import FormAPITestBase
from abroadin.apps.estimation.form.models import StudentDetailedInfo

User = get_user_model()


class FormAPITests(FormAPITestBase):

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
                "grades": [self.master_grade.id, self.phd_grade.id],
                "majors": [self.major1.id, self.major2.id],
                "semester_years": [self.semester_year1.id, self.semester_year2.id]
            },
            "educations": [
                {
                    "graduate_in": 2020,
                    "thesis_title": None,
                    "major": self.major3.id,
                    "grade": GradeChoices.BACHELOR.value,
                    "university": self.university2.id,
                    "gpa": "19.00"
                },
                {
                    "graduate_in": 2018,
                    "thesis_title": "Be to che",
                    "major": self.major4.id,
                    "grade": GradeChoices.MASTER.value,
                    "university": self.university5.id,
                    "gpa": "18.00"
                }
            ],
            "publications": [
                {
                    "journal_reputation": Publication.JournalReputationChoices.FOUR_TO_TEN.value,
                    "publish_year": 2020,
                    "which_author": Publication.WhichAuthorChoices.SECOND.value,
                    "type": Publication.PublicationChoices.JOURNAL.value,
                    "title": "sdfsdf"
                },
                {
                    "journal_reputation": Publication.JournalReputationChoices.ONE_TO_THREE.value,
                    "publish_year": 2018,
                    "which_author": Publication.WhichAuthorChoices.FIRST.value,
                    "type": Publication.PublicationChoices.CONFERENCE.value,
                    "title": "ffff"
                }
            ],
            "language_certificates": [
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": False,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.TOEFL.value,
                        'speaking': 23,
                        'listening': 23,
                        'writing': 23,
                        'reading': 23,
                        'overall': 102,
                    },
                },
                {
                    'class_type': 'applydata__regularlanguagecertificate',
                    'data': {
                        "is_mock": True,
                        "certificate_type": LanguageCertificate.LanguageCertificateType.IELTS_GENERAL.value,
                        'speaking': 5,
                        'listening': 5,
                        'writing': 5,
                        'reading': 5,
                        'overall': 6,
                    }
                }
            ],
            "payment_affordability": None,
            "prefers_full_fund": None,
            "prefers_half_fund": None,
            "prefers_self_fund": None,
            "comment": "",
            "powerful_recommendation": False,
            "linkedin_url": None,
            "homepage_url": None
        }

    def _test_form_list(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:student-detailed-info-list', *args, **kwargs)

    def _test_form_detail(self, *args, **kwargs):
        return self._endpoint_test_method('estimation.form:student-detailed-info-detail', *args, **kwargs)

    def test_form_list_post_201(self):
        self.student_detailed_info1.delete()
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)

    def test_form_list_post_401_1(self):
        self.student_detailed_info1.delete()
        res = self._test_form_list("post", None, status.HTTP_401_UNAUTHORIZED, data=self.payload)

    def test_form_list_post_403_2(self):
        self.student_detailed_info1.delete()
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED, data=self.payload)

        self._test_form_list("post", self.user1, status.HTTP_403_FORBIDDEN, data=self.payload)

    def test_form_list_post_400(self):
        self.student_detailed_info1.delete()
        self._test_form_list("post", self.user1, status.HTTP_400_BAD_REQUEST)

    def test_form_detail_get_401(self):
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("get", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.student_detailed_info1.id)

    def test_form_detail_get_403(self):
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("get", self.user2, status.HTTP_403_FORBIDDEN,
                               reverse_args=self.student_detailed_info1.id)

    def temporary_deprecated_test_form_detail_put_patch_200(self):
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

    def temporary_deprecated_test_form_detail_put_patch_401(self):
        self._test_form_detail("put", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("patch", None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.student_detailed_info1.id)

    def temporary_deprecated_test_form_detail_put_patch_403(self):
        self._test_form_detail("put", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id)
        self._test_form_detail("patch", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=self.student_detailed_info1.id)
