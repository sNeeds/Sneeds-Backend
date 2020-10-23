from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from abroadin.apps.estimation.tests.apis import EstimationBaseTest
from abroadin.apps.estimation.form.models import StudentDetailedInfo, Grade, WantToApply, SemesterYear
from abroadin.apps.data.account.models import Country, University, Major

User = get_user_model()


class FormAPITests(EstimationBaseTest):

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
        if response.status_code != expected_status:
            print("AssertionError occurred, Response data: ", response.data)
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

    def test_form_detail_get_200(self):
        data = self._test_form_list("post", None, status.HTTP_201_CREATED)
        self._test_form_detail("get", self.user1, status.HTTP_200_OK, reverse_args=data['id'])
        self._test_form_detail("get", None, status.HTTP_200_OK, reverse_args=data['id'])

    def test_form_detail_put_patch_200(self):
        def _update_all_fields(update_method, update_fields):
            data = self._test_form_list("post", self.user1, status.HTTP_201_CREATED)
            for k, v in update_fields.items():
                data = self._test_form_detail(update_method, self.user1, status.HTTP_200_OK, reverse_args=data['id'],
                                              data={k: v}, )

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
        self._test_form_detail("put", self.user1, status.HTTP_200_OK, reverse_args=data['id'])
        self._test_form_detail("patch", self.user1, status.HTTP_200_OK, reverse_args=data['id'])
        self._test_form_detail("put", None, status.HTTP_401_UNAUTHORIZED, reverse_args=data['id'])
        self._test_form_detail("patch", None, status.HTTP_401_UNAUTHORIZED, reverse_args=data['id'])
        self._test_form_detail("put", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=data['id'])
        self._test_form_detail("patch", self.user2, status.HTTP_403_FORBIDDEN, reverse_args=data['id'])

