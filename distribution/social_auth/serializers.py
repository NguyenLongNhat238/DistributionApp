from pytz import NonExistentTimeError
from rest_framework import serializers
from . import google, facebook
from .services import register_social_google_user, register_social_facebook_user
from rest_framework.exceptions import AuthenticationFailed
# from constant.choice import GOOGLE_CLIENT_ID


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # if user_data['aud'] != GOOGLE_CLIENT_ID:   # note HERE
        #     raise AuthenticationFailed('google client id not right')

        # user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        print(name, email)
        # print(user_data) # {'iss': 'https://accounts.google.com', 'azp': '407408718192.apps.googleusercontent.com', 'aud': '407408718192.apps.googleusercontent.com', 'sub': '100341342189162789244', 'email': 'tienle676@gmail.com', 'email_verified': True, 'at_hash': 'KKgvDVtmpYA01qdFCfnSQA', 'name': 'Tiến Lê', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14GhX0i1cNpso8Ufilymd2Jgfkn6I1Z7mjBvo_MEUWw=s96-c', 'given_name': 'Tiến', 'family_name': 'Lê', 'locale': 'vi', 'iat': 1628390059, 'exp': 1628393659}
        return register_social_google_user(email=email, name=name)


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        # print(user_data)  # {'name': 'Tiến', 'email': 'tienle676@gmail.com', 'id': '1445903722433638'}
        try:
            if 'email' not in user_data.keys():
                raise serializers.ValidationError(
                    {'error': 'Tài khoản của bạn không cung cấp tài khoản email cho chúng tôi. Vui lòng chọn cách đăng nhập khác.'})
        except:
            pass
        try:
            email = user_data['email']
            name = user_data['name']
            return register_social_facebook_user(email=email, name=name)

        except Exception as identifier:

            raise serializers.ValidationError({
                'error': 'The token  is invalid or expired. Please login again.'
            })
