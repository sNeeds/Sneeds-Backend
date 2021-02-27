from django.contrib.auth import get_user_model

from abroadin.apps.users.customAuth.models import CustomUser
from .base import SocialAuthFunctionTestBase
from ...register import _register_user, get_jwt_tokens, login_register_social_user

User = get_user_model()


class RegisterFunctionsTests(SocialAuthFunctionTestBase):
    def setUp(self):
        super().setUp()

    def test__register_user__ok(self):
        func = _register_user
        data = {
            'email': 'b@a.com',
            'password': '111111',
            'first_name': 'foo',
            'last_name': 'bar',
            'phone_number': '+989127170060',
            'auth_provider': CustomUser.AuthProviderTypeChoices.GOOGLE
        }
        user = func(**data)

        self.assertEqual(user.email, 'b@a.com')
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.first_name, 'foo')
        self.assertEqual(user.last_name, 'bar')
        self.assertEqual(user.phone_number, '+989127170060')
        self.assertEqual(user.auth_provider, CustomUser.AuthProviderTypeChoices.GOOGLE)

    def test__register_user__only_email_password(self):
        func = _register_user
        data = {
            'email': 'b@a.com',
            'password': '111111',
        }
        user = func(**data)

        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.email, 'b@a.com')

    def test_get_jwt_tokens__ok(self):
        func = get_jwt_tokens

        user = self.user1
        data = func(user)

        self.assertIsNotNone(data['access'])
        self.assertIsNotNone(data['refresh'])

    def test_login_register_social_user__new_user(self):
        func = login_register_social_user

        tokens = func(
            email='a@b.com',
            provider=CustomUser.AuthProviderTypeChoices.GOOGLE,
            first_name='foo',
            last_name='bar'
        )

        self.assertIsNotNone(tokens['access'])
        self.assertIsNotNone(tokens['refresh'])
        self.assertEqual(User.objects.filter(email='a@b.com'), 1)
