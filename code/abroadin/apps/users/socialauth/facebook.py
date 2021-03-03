import facebook

from abroadin.settings.secure.APIs import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET


class Facebook:

    @staticmethod
    def validate(auth_token):
        graph = facebook.GraphAPI()
        access_token = graph.get_access_token_from_code(
            code=auth_token,
            redirect_uri='https://abroadin.com/auth/oauth2/facebook',
            app_id=FACEBOOK_CLIENT_ID,
            app_secret=FACEBOOK_CLIENT_SECRET
        )['access_token']

        graph = facebook.GraphAPI(access_token=access_token)
        profile = graph.request('/me?fields=first_name,last_name,email')
        return profile
