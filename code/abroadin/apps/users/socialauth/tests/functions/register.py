from abroadin.apps.users.customAuth.models import CustomUser
from .base import SocialAuthFunctionTestBase
from ...register import _register_user


class RegisterFunctionsTests(SocialAuthFunctionTestBase):
    def setUp(self):
        super().setUp()

    def test__register_user__ok(self):
        function = _register_user
        data = {
            'email': 'b@a.com',
            'password': '111111',
            'first_name': 'foo',
            'last_name': 'bar',
            'phone_number' : '+989127170060',
            'provider' : CustomUser.AuthProviderTypeChoices.GOOGLE
        }
        user = function(data)

        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.email, 'b@a.com')
        self.assertEqual(user.is_verified, '111111')
        self.assertEqual(user.first_name, 'foo')
        self.assertEqual(user.last_name, 'bar')
        self.assertEqual(user.phone_number, '+989127170060')
        self.assertEqual(user.provider, '+989127170060')

    def test__register_user__only_email_password(self):
        function = _register_user
        data = {
            'email': 'b@a.com',
            'password': '111111',
        }
        user = function(data)

        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.email, 'b@a.com')
        self.assertEqual(user.is_verified, '111111')

    def test_login_register_social_user(self):
