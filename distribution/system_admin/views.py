from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserRole, Permission
from user.models import User
from .serializers import (
    UserRoleListSerializer,
    UserRoleSerializer,
    PermissionSerializer,
    UserSerializer,
    CreateNewUserSerializer,
    ListUserSerializer,
)
from .permissions import SystemAdminPermission
from core_app.res_handing import SuccessHandling

# Create your views here.


class PermissionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [SystemAdminPermission]
    filter_fields = ["name", "code"]


class UserRoleViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [SystemAdminPermission]

    def get_serializer_class(self):
        if self.action == "list":
            return UserRoleListSerializer
        return super().get_serializer_class()


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [SystemAdminPermission]

    def get_serializer_class(self):
        if self.action == "list":
            return ListUserSerializer
        if self.action == "create":
            return CreateNewUserSerializer
        return super().get_serializer_class()

    def get_object(self):
        return super().get_object()

    def get_queryset(self):
        query = User.objects.filter(company=self.request.user.company)
        return query

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            SuccessHandling(
                message_en="Create new user successfully",
                message_vi="Tạo người dùng mới thành công",
                code=201,
            ).to_representation(),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["post"], url_path="deactive-user")
    def deactive_user(self, request, obj):
        """
        deactive user
        """
        obj.is_active = False
        obj.save()
        return Response(
            SuccessHandling(
                message_en="Deactive user successfully",
                message_vi="Vô hiệu hóa người dùng thành công",
                code=200,
            ).to_representation(),
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="reset-user-password")
    def reset_user_password(self, request, obj):
        """
        reset user password
        """
        obj.set_password("123456")
        obj.save()
        return Response(
            SuccessHandling(
                message_en="Reset user password successfully",
                message_vi="Đặt lại mật khẩu người dùng thành công",
                code=200,
            ).to_representation(),
            status=status.HTTP_200_OK,
        )
