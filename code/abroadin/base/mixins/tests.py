from django.urls import reverse


class TestBriefMethodMixin:
    def _endpoint_test_method(
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
