from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from apps.estimation.form.models import StudentDetailedInfo

User = get_user_model()


class StudentDetailedInfoTests(EstimationBaseTest):

    def setUp(self):
        super().setUp()

    def _test_form(
            self,
            reverse_str,
            method,
            user,
            expected_status,
            reverse_args=None,
            *args,
            **kwargs
    ):
        if reverse_args:
            url = reverse(reverse_str, args=[reverse_args])
        else:
            url = reverse(reverse_str)

        client = self.client

        if user:
            client.force_login(user)

        response = getattr(client, method)(url, *args, **kwargs)
        self.assertEqual(response.status_code, expected_status)

        return response.data

    def _test_form_list(self, *args, **kwargs):
        return self._test_form('estimation.form:student-detailed-info-list', *args, **kwargs)

    def _test_form_detail(self, *args, **kwargs):
        return self._test_form('estimation.form:student-detailed-info-detail', *args, **kwargs)

    def test_form_list_post_201(self):
        self._test_form_list("post", None, status.HTTP_201_CREATED)
        self._test_form_list("post", None, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED, data={"age": 20}, )

    def test_form_list_post_403(self):
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_403_FORBIDDEN)

    def test_form_detail_put_200(self):
        update_these = {
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
            "linkedin_url": "https://www.linkedin.com/in/arya-khaligh/",
            "homepage_url": "https://www.aryakhaligh.ir/",
        }

        data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        for k, v in update_these.items():
            self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'], data={k: v}, )
        #
        # obj = StudentDetailedInfo.objects.filter(id=data['id'])
        # self.assertEqual(obj.age, data['age'])
        # self.assertEqual(obj.related_work_experience, data['related_work_experience'])
        # self.assertEqual(obj.academic_break, data['academic_break'])
        # self.assertEqual(obj.olympiad, data['olympiad'])
        # self.assertEqual(obj.gender, data['gender'])
        # self.assertEqual(obj.is_married, data['age'])
        # self.assertEqual(obj.age, data['age'])
        # self.assertEqual(obj.age, data['age'])
        #
        # data = self._test_form_list("post", None, status.HTTP_201_CREATED)
        # self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
        #                        data={"homepage_url": "https://www.aryakhaligh.ir/"}, )
