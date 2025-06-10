from accounts.models import Company, Employee, Customer
from common.serializers import BaseSerializer


class CompanySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Company
        fields = '__all__'
        read_only_fields = ['id']


class EmployeeSerializer(BaseSerializer):

    class Meta(BaseSerializer.Meta):
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'contact', 'email', 'role', 'company']
        extra_kwargs = {
            **BaseSerializer.Meta.extra_kwargs,
            'password': {'write_only': True}
        }


class CustomerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']


