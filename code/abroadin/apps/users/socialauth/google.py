from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request()
            )
        except Exception as e:
            raise GoogleAuthError(e.__str__())

        if 'accounts.google.com' not in idinfo['iss']:
            raise GoogleAuthError('Wrong iss in idinfo')

        return idinfo
