from django.contrib.auth import authenticate
from user.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from constant.choice import DEFAULT_PASSWORD


def register_social_google_user(email, name):

    try:
        # check user has email is exist
        user = User.objects.get(email=email)
        if user.auth_google == False:
            user.is_active = True
            user.auth_google = True
            user.save()

        return {
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }

    except:
        # check user has email is not exist
        # make new phone randomly
        try:
            while True:
                new_phone = "000" + \
                    "".join([str(random.randint(0, 9)) for i in range(7)])
                user = User.objects.get(phone=new_phone)
        except:
            pass
        print("sdfsdfsdsdfsdfsdf: ", new_phone)
        sex = "male"
        role = "member"

        # if condition of sex:
        #     sex = ""
        # if condition of role:
        #     role = ""

        new_user = User.objects.create_user(
            username=name,
            sex=sex,
            phone=new_phone,
            email=email,
            # role=role
        )
        new_user.set_password(DEFAULT_PASSWORD)
        new_user.is_active = True
        new_user.auth_google = True
        new_user.save()
        return {
            'access_token': new_user.access_token,
            'refresh_token': new_user.refresh_token
        }


def register_social_facebook_user(email, name):

    try:
        # check user has email is exist
        user = User.objects.get(email=email)
        if user.auth_facebook == False:
            user.is_verified = True
            user.is_active = True
            user.auth_facebook = True
            user.save()

        return {
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }

    except:
        # check user has email is not exist
        new_user = User.objects.create_user(
            username=name, email=email, password=DEFAULT_PASSWORD)
        new_user.is_verified = True
        new_user.is_active = True
        new_user.auth_facebook = True
        new_user.save()
        return {
            'access_token': new_user.access_token,
            'refresh_token': new_user.refresh_token
        }
