import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from common.models import BaseModel


class Company(BaseModel):
    """
    This model creates a company in the system
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9][a-zA-Z0-9\s\-&]*$',
                message=(
                    'Company name must start with a letter or number and can only contain '
                    'letters, numbers, spaces, hyphens (-), and ampersands (&).'
                )
            )
        ]
    )
    address = models.TextField(null=False, blank=False, validators=[RegexValidator(
        r'^[0-9a-zA-Z\s.,#-]+$',
        "Address can only contain letters, numbers, spaces, and ., #, -."
    )])
    company_email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=13, unique=True, null=False, blank=False, validators=[RegexValidator(
        r'^(0[2356][0-9]{8}|(\+233|233)[2356][0-9]{7})$',
        "Enter a valid Ghanaian phone number."
    )])

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return self.name


class Customer(BaseModel):
    """
    This is the model for creating a customer in a company.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=False, blank=False, validators=[RegexValidator(
        r"^[a-zA-Z]+(?:['-][a-zA-Z]+)?$",
        "Enter a valid first name. First names can only contain letters, hyphens, or apostrophes."
    )])
    last_name = models.CharField(max_length=100, validators=[RegexValidator(
        r"^[a-zA-Z]+(?:['-][a-zA-Z]+)?$",
        "Enter a valid last name. Last names can only contain letters, hyphens, or apostrophes."
    )])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, unique=True, validators=[RegexValidator(
        r'^(0[2356][0-9]{8}|(\+233|233)[2356][0-9]{7})$',
        "Enter a valid Ghanaian phone number."
    )])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class EmployeeManager(BaseUserManager):
    # to account for using email for authentication
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Employee(AbstractUser, BaseModel):
    """
    This is the model for creating an employee in a company.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
    ]

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=13, null=False, validators=[RegexValidator(
        r'^(0[2356][0-9]{8}|(\+233|233)[2356][0-9]{7})$',
        "Enter a valid Ghanaian phone number."
    )])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(
        Group,
        related_name='employee_groups',  # Unique related_name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_permissions',  # Unique related_name for permissions
        blank=True
    )

    objects = EmployeeManager()

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return self.full_name

    def clean(self):
        # ensure company requirement for non-superusers
        if not self.is_superuser:
            raise ValidationError('Company is required for non-superusers')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
