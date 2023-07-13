from rest_framework.decorators import action
from rest_framework import viewsets, permissions, generics, status
from core_app.views import (
    ActionImportExcelViewSet,
    BaseModelViewSet,
    ActionExportExcelViewSet,
)
from information_management.models import Company, Customer, Employee, Supplier, Channel
from information_management.permissions import (
    BlockedPermission,
    EmployeePermissions,
    ManagerCompanyPermissions,
)
from information_management.serializers import (
    ChannelSerializer,
    CompanyDetailSerializer,
    CompanySerializer,
    CustomerSerializer,
    CustomerDetailSerializer,
    EmployeeDetailSerializer,
    EmployeeSerializer,
    SupplierDetailSerializer,
    SupplierSerializer,
)

# Create your views here.


class CompanyViewSet(BaseModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    model = Company
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return CompanyDetailSerializer
        return CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(manager=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "patch"]:
            return [ManagerCompanyPermissions()]
        if self.action in ["create"]:
            return [BlockedPermission()]
        return [permissions.IsAuthenticated()]


class CustomerViewSet(
    BaseModelViewSet, ActionImportExcelViewSet, ActionExportExcelViewSet
):
    queryset = Customer.company_objects.all()
    serializer_class = CustomerSerializer
    import_serializer_class = CustomerSerializer
    export_serializer = CustomerSerializer
    model = Customer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        print(self.request.user)
        if self.action in ["retrieve"]:
            return CustomerDetailSerializer
        return CustomerSerializer

    def get_queryset(self):
        query = Customer.company_objects.all()
        return query


class EmployeeViewSet(
    BaseModelViewSet, ActionImportExcelViewSet, ActionExportExcelViewSet
):
    queryset = Employee.company_objects.all()
    serializer_class = EmployeeSerializer
    import_serializer_class = EmployeeSerializer
    export_serializer = EmployeeDetailSerializer
    model = Employee
    # pagination_class = ListPaginator
    permission_classes = [EmployeePermissions]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def get_permissions(self):
        return [EmployeePermissions()]


class SupplierViewSet(
    BaseModelViewSet, ActionImportExcelViewSet, ActionExportExcelViewSet
):
    queryset = Supplier.company_objects.all()
    serializer_class = SupplierSerializer
    import_serializer_class = SupplierSerializer
    export_serializer = SupplierDetailSerializer
    model = Supplier
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return SupplierDetailSerializer
        return SupplierSerializer


class ChannelViewSet(BaseModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    model = Channel
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return ChannelSerializer

    def get_queryset(self):
        return Channel.objects.all()
