from rest_framework import serializers
from user.models import User
from .models import UserRole, Permission
from user import password_validation as custom_password_validation
from core_app.res_handing import ErrorHandling


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        read_only = True
        model = Permission
        fields = ["id", "name"]


class UserRoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["id", "name", "code"]


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["id", "name", "code", "permissions", "description"]


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "role"]


class UserSerializer(ListUserSerializer):
    class Meta:
        model = ListUserSerializer.Meta.model
        fields = ListUserSerializer.Meta.fields + [
            "first_name",
            "last_name",
            "avatar",
            "identity_card",
            "address",
            "birthday",
        ]


class CreateNewUserSerializer(serializers.ModelSerializer):
    """
    create new user if data is validated,
    """

    company = None

    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "phone",
            "email",
            "role",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user = self.context["request"].user
        self.company = user.company
        password = data["password"]
        confirm_password = data["confirm_password"]
        phone = data["phone"]

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                ErrorHandling(
                    message_en="This phone number has already been used.",
                    message_vi="Số điện thoại này đã được sử dụng.",
                    code=400,
                ).to_representation()
            )
        email = data["email"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                ErrorHandling(
                    message_en="This email has already been used.",
                    message_vi="Email này đã được sử dụng.",
                    code=400,
                ).to_representation()
            )
        error = custom_password_validation.validate_password(password=password)
        # Method inherited from BaseForm
        if error:
            raise serializers.ValidationError(
                ErrorHandling(
                    message_en=error, message_vi=error, code=400
                ).to_representation()
            )
        if "confirm_password" in data.keys():
            if password != confirm_password:
                raise serializers.ValidationError(
                    ErrorHandling(
                        message_en="Password and confirm password must be the same.",
                        message_vi="Mật khẩu và xác nhận mật khẩu phải giống nhau.",
                        code=400,
                    ).to_representation()
                )
        elif confirm_password is None:
            raise serializers.ValidationError(
                ErrorHandling(
                    message_en="You have not entered the confirm password.",
                    message_vi="Bạn chưa nhập lại mật khẩu.",
                ).to_representation()
            )
        return super().validate(data)

    def create(self, validated_data):
        """
        create new user
        """
        password = validated_data["password"]
        new_user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            company=self.company,
        )
        new_user.set_password(password)
        new_user.is_active = True
        new_user.role = validated_data["role"]
        new_user.save()

        return new_user
