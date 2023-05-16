from rest_framework.decorators import action
from rest_framework import viewsets, permissions, generics, status
from core_app.views import ActionImportExcelViewSet, BaseModelViewSet
from information_management.models import Company, Customer, Employee, Supplier
from information_management.permissions import ManagerCompanyPermissions
from information_management.serializers import CompanyDetailSerializer, CompanySerializer, CustomerSerializer, CustomerDetailSerializer, EmployeeDetailSerializer, EmployeeSerializer, SupplierDetailSerializer, SupplierSerializer
# Create your views here.


class CompanyViewSet(BaseModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return CompanyDetailSerializer
        return CompanySerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update', 'patch']:
            return [ManagerCompanyPermissions()]
        return [permissions.IsAuthenticated()]


class CustomerViewSet(BaseModelViewSet, ActionImportExcelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    import_serializer_class = CustomerSerializer
    model = Customer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return CustomerDetailSerializer
        return CustomerSerializer


class EmployeeViewSet(BaseModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return EmployeeDetailSerializer
        return EmployeeSerializer


class SupplierViewSet(BaseModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return SupplierDetailSerializer
        return SupplierSerializer
