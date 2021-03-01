import requests
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as transport_requests
from google.oauth2 import id_token

from abroadin.settings.secure.APIs import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        data = {
            'code': auth_token,
            'redirect_uri': 'https://abroadin.com/auth/login',
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'grant_type': 'authorization_code',
        }
        exchange = requests.post(
            'https://oauth2.googleapis.com/token',
            data=data
        ).json()

        access_token = exchange['access_token']

        try:
            idinfo = id_token.verify_oauth2_token(
                access_token, transport_requests.Request()
            )
        except Exception as e:
            raise GoogleAuthError(e.__str__())

        if 'accounts.google.com' not in idinfo['iss']:
            raise GoogleAuthError('Wrong iss in idinfo')

        return idinfo
