from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest

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
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED)

    def test_form_list_post_403(self):
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_403_FORBIDDEN)

    def test_form_detail_put_200(self):
        data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"age": 20}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"related_work_experience": 5}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"academic_break": 5}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"olympiad": 5}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"gender": "Male"}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"is_married": True}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"payment_affordability": "Average"}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"prefers_full_fund": True}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"prefers_half_fund": False}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"prefers_self_fund": True}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"comment": "Foo comment"}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"powerful_recommendation": False}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"linkedin_url": "https://www.linkedin.com/in/arya-khaligh/"}, )
        self._test_form_detail("put", self.user1, status.HTTP_200_FORBIDDEN, reverse_args=data['id'],
                               data={"homepage_url": "https://www.aryakhaligh.ir/"}, )
