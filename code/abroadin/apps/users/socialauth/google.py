import google_auth_oauthlib.flow

from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as transport_requests
from google.oauth2 import id_token
from oauthlib.oauth2 import OAuth2Error

from abroadin.settings.secure.APIs import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def credentials_to_dict(credentials):
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'id_token': credentials.id_token,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        client_conf = {
            "web":
                {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
        }

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_conf,
            scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid'
            ],
        )
        flow.redirect_uri = 'https://abroadin.com/auth/oauth2/google'

        try:
            flow.fetch_token(code=auth_token)
        except OAuth2Error as e:
            raise GoogleAuthError(e.__str__())

        credentials = Google.credentials_to_dict(flow.credentials)

        id_token_code = credentials['id_token']

        try:
            id_info = id_token.verify_oauth2_token(
                id_token_code, transport_requests.Request()
            )
        except Exception as e:
            raise GoogleAuthError(e.__str__())

        if 'accounts.google.com' not in id_info['iss']:
            raise GoogleAuthError('Wrong iss in id_info')

        return id_info
