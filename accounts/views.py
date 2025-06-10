import random, string, logging

from django.contrib.auth.hashers import make_password
from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from laundry_api.settings import EMAIL_HOST_USER
from accounts.models import Company, Employee, Customer
from accounts.serializers import CompanySerializer, EmployeeSerializer, CustomerSerializer
from common.viewsets import CustomViewSet

logger = logging.getLogger(__name__)

class CompanyViewSet(CustomViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    search_fields = ['id', 'name', 'address']
    ordering_fields = ['id', 'name', 'address']
    permission_classes = [permissions.AllowAny]


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a company and its admin employee
        in a single transaction.
        """

        data = request.data

        # Prepare company data
        company_data = {
            "name": data.get("name"),
            "address": data.get("address"),
            "company_email": data.get("company_email"),
            "phone": data.get("phone"),
        }

        # Prepare admin employee data
        employee_data = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "contact": data.get("contact"),
            "password": data.get("password"),
            "role": "ADMIN",
        }

        try:
            # Validate and create the company
            company_serializer = CompanySerializer(data=company_data)
            company_serializer.is_valid(raise_exception=True)
            company = company_serializer.save()

            # Attach the company to the admin employee data
            employee_data["company"] = company.pk
            employee_serializer = EmployeeSerializer(data=employee_data)
            employee_serializer.is_valid(raise_exception=True)

            # Create the admin employee with hashed password
            admin_employee = employee_serializer.save()
            admin_employee.set_password(employee_data["password"])
            admin_employee.is_staff = True
            admin_employee.save()

            # Send welcome email to the admin

            try:
                send_mail(
                subject="Welcome to Jemma",
                message=(
                    f"Dear {admin_employee.first_name},\n\n"
                    f"Your admin account for the company '{company.name}' has been successfully created.\n\n"
                    f"Thank you for choosing Jemma Technologies!"
                ),
                from_email=settingsEMAIL_HOST_USER,
                recipient_list=[admin_employee.email],
                fail_silently=False,
            )
            except Exception as e:
                print(f"Error : {e}")

            return Response(
                {
                    "company": company_serializer.data,
                    "admin_employee": EmployeeSerializer(admin_employee).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except BadRequest as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_superuser:
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "You do not have permission to view this information."},
            status=status.HTTP_403_FORBIDDEN
        )

    # def retrieve(self, request, pk=None):
    #
    #     try:
    #         company = Company.objects.get(pk=pk)
    #         if
    #
    #     except Company.DoesNotExist:
    #         return Response(
    #             {
    #                 "message": "Company does not exist.",
    #             },
    #             status=status.HTTP_404_NOT_FOUND
    #         )


class EmployeeViewSet(CustomViewSet):
    serializer_class = EmployeeSerializer
    search_fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'role']
    ordering_fields = search_fields
    filterset_fields = search_fields  # for filtering

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            # Check if password is provided, if not, generate a random password
            password = self.request.data.get('password')
            if not password:
                password = self.generate_random_password()

            # Save the employee with the password
            employee = serializer.save(company=self.request.user.company)
            self.send_invitation_email(employee, password)

            employee.password = make_password(password)
            employee.save()

        except Exception as e:
            transaction.set_rollback(True)
            raise e

    def get_queryset(self):
        return Employee.objects.filter(company=self.request.user.company)

    def generate_random_password(self):
        """Generate a random password with uppercase, lowercase, digits, and special characters."""
        length = 12  # You can adjust the password length
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def send_invitation_email(self, employee, password):
        """
        Sends an email to the new employee to reset their password
        """

        subject = "Welcome to Jemma Laundry System!"
        message = (f"Dear {employee.first_name},\n\n"
                   f"Your account has been created for the Jemma system. "
                   f"Here are your login details:\n\n"
                   f"Email: {employee.email}\n"
                   f"Password: {password}\n\n"
                   f"Please login and change your password as soon as possible.\n\n"
                   f"Thank you,\nJemma Technologies")

        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [employee.email],
            fail_silently=False
        )


class CustomerViewSet(CustomViewSet):
    serializer_class = CustomerSerializer
    search_fields = ['id', 'first_name', 'last_name', 'email']
    ordering_fields = ['id', 'first_name', 'last_name', 'email']
    filterset_fields = search_fields

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or not hasattr(self.request.user, 'company'):
            raise PermissionDenied("You must be authenticated and associated with a company to create a customer.")
        serializer.save(company=self.request.user.company)

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)
