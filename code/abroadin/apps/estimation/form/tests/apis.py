from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo

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
        else:
            client.logout()

        response = getattr(client, method)(url, *args, **kwargs)
        self.assertEqual(response.status_code, expected_status)

        return response.data

    def _test_form_list(self, *args, **kwargs):
        return self._test_form('estimation.form:student-detailed-info-list', *args, **kwargs)

    def _test_form_detail(self, *args, **kwargs):
        return self._test_form('estimation.form:student-detailed-info-detail', *args, **kwargs)

    def test_form_list_post_201(self):
        self._test_form_list("post", None, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED, data={"age": 20}, )
        self._test_form_list("post", None, status.HTTP_201_CREATED)

    def test_form_list_post_403(self):
        self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user2, status.HTTP_201_CREATED)
        self._test_form_list("post", self.user1, status.HTTP_403_FORBIDDEN)

    def test_form_detail_put_patch_200(self):
        update_fields = {
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

        data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
        for k, v in update_fields.items():
            data = self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'], data={k: v}, )

        obj = StudentDetailedInfo.objects.get(id=data['id'])
        for k in update_fields.keys():
            self.assertEqual(getattr(obj, k), data[k])
            self.assertEqual(getattr(obj, k), update_fields[k])

        data = self._test_form_list("post", None, status.HTTP_201_CREATED)
        self.assertEqual(data["user"], None)

        self._test_form_detail("put", self.user2, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"homepage_url": "https://www.kati.com/"}, )
        self.assertEqual(data["user"]["id"], self.user2.id)
        self.assertEqual(data["homepage_url"], "https://www.kati.com/")

        self._test_form_detail("patch", self.user2, status.HTTP_200_OK, reverse_args=data['id'],
                               data={"homepage_url": "https://www.foo.com/"}, )
        self.assertEqual(data["homepage_url"], "https://www.foo.com/")

        obj = StudentDetailedInfo.objects.get(id=data['id'])
        self.assertEqual(obj.homepage_url, "https://www.foo.com/")
