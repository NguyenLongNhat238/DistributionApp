from django.contrib.auth import authenticate
import requests
from user.models import User
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework.exceptions import AuthenticationFailed
from constant.choice import DEFAULT_PASSWORD
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib.common import generate_token
from datetime import  timedelta
from django.utils import timezone


def register_social_google_user(email, name, avatar):
    user, created = User.objects.get_or_create(email=email)
    if created is True:
        user.username = name
        user.sex = user.SEX_MALE
        user.set_password(DEFAULT_PASSWORD)
        user.save()

    if bool(user.avatar) is False:
        try:
            # Download picture and set avatar
            response = requests.get(avatar)
            avatar_data = response.content
            user.avatar.save("avatar.jpg", ContentFile(avatar_data))
        except:
            print("Can't get picture from account google")

    if not user.auth_google:
        user.is_active = True
        user.auth_google = True
        user.save()
    role = "user"
    # role = user.selected_roles
    if user.is_superuser or user.is_staff:
        role = "admin"

    app = Application.objects.get(name="Social Auth")
    token = generate_token()
    refresh_token = generate_token()
    expires = AccessToken.objects.create(
        user=user,
        application=app,
        token=token,
        expires=timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS),
        scope="read write",
    )
    RefreshToken.objects.create(
        token=refresh_token, access_token=expires, application=app, user=user
    )
    return {
        "id": user.id,
        "access_token": token,
        "refresh_token": refresh_token,
        "scope": expires.scope,
        "expires": settings.TOKEN_EXPIRE_SECONDS,
    }
    # return {
    #     "id": user.id,
    #     "access_token": user.access_token,
    #     "refresh_token": user.refresh_token,
    #     "role": role,
    #     "expires": user.expires,
    # }


def register_social_facebook_user(fb_id, email, name, first_name, last_name, avatar):
    user, created = User.objects.get_or_create(fb_id=fb_id)
    if created is True:
        user.is_verified = True
        user.is_active = True
        user.auth_facebook = True
        user.username = name
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.sex = user.SEX_MALE
        user.set_password(DEFAULT_PASSWORD)
        user.save()

    if bool(user.avatar) is False:
        try:
            # Download picture and set avatar
            response = requests.get(avatar)
            avatar_data = response.content
            user.avatar.save(f"fb_avatar_{fb_id}.jpg", ContentFile(avatar_data))
        except:
            print("Can't get picture from account facebook")

    if not user.auth_facebook:
        user.is_verified = True
        user.is_active = True
        user.auth_facebook = True
        user.save()
    role = None
    # role = user.selected_roles
    if user.is_superuser or user.is_staff:
        role = "admin"
    app = Application.objects.get(name="Social Auth")
    token = generate_token()
    refresh_token = generate_token()
    expires = AccessToken.objects.create(
        user=user,
        application=app,
        token=token,
        expires=timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS),
        scope="read write",
    )
    RefreshToken.objects.create(
        token=refresh_token, access_token=expires, application=app, user=user
    )
    return {
        "id": user.id,
        "access_token": token,
        "refresh_token": refresh_token,
        "scope": expires.scope,
        "expires": settings.TOKEN_EXPIRE_SECONDS,
    }
    # return {
    #     "id": user.id,
    #     "access_token": user.access_token,
    #     "refresh_token": user.refresh_token,
    #     "role": role,
    #     "expires": user.expires,
    # }
