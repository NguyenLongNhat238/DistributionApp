from .settings import oauth2_settings
import re


class BaseScopes:
    def get_all_scopes(self):
        """
        Return a dict-like object with all the scopes available in the
        system. The key should be the scope name and the value should be
        the description.

        ex: {"read": "A read scope", "write": "A write scope"}
        """
        raise NotImplementedError("")

    def get_available_scopes(self, application=None, request=None, *args, **kwargs):
        """
        Return a list of scopes available for the current application/request.

        TODO: add info on where and why this method is called.

        ex: ["read", "write"]
        """
        raise NotImplementedError("")

    def get_default_scopes(self, application=None, request=None, *args, **kwargs):
        """
        Return a list of the default scopes for the current application/request.
        This MUST be a subset of the scopes returned by `get_available_scopes`.

        TODO: add info on where and why this method is called.

        ex: ["read"]
        """
        raise NotImplementedError("")


class SettingsScopes(BaseScopes):
    def get_all_scopes(self):
        return oauth2_settings.SCOPES

    def get_available_scopes(self, application=None, request=None, *args, **kwargs):
        # return {
        #     "read": "Read scope",
        #     "write": "Write scope",
        #     "groups": "Access to your groups",
        #     "profile": "Access to your profile",
        #     "email": "Access to your email address",
        # }
        return oauth2_settings._SCOPES

    def get_default_scopes(self, application=None, request=None, *args, **kwargs):
        # print("SANITIZED request:")
        # print("URL:", request.uri)
        # print("HTTP Method:", request.http_method)
        # print("Headers:", request.headers)
        # print("Body:", request.body)
        # if request.uri == "/oauth/auth-token/":
        #     match = re.search(r"grant_type=([^&]+)", request.body)
        #     grant_type = match.group(1) if match else None
        #     if grant_type in ["password", "refresh_token"]:
        #         return ["read", "write", "groups", "profile", "email"]
        return oauth2_settings._DEFAULT_SCOPES


def get_scopes_backend():
    scopes_class = oauth2_settings.SCOPES_BACKEND_CLASS
    return scopes_class()
