from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from accounts.models import Company
from common.models import BaseModel


class Service(BaseModel):
    """
    This class defines the services of the laundry
    """
    name = models.CharField(max_length=100, validators=[RegexValidator(
                r'^[a-zA-Z]+(?:[ \'-][a-zA-Z]+)*$',
                "Enter a valid service name. Service names can only contain letters, spaces, hyphens, or apostrophes."
    )])
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return f'Name: {self.name}'


class Item(BaseModel):
    """
    This model defines the item and its price with respect to the service
    """
    name = models.CharField(max_length=100, validators=[RegexValidator(
                r'^[a-zA-Z]+(?:[ \'-][a-zA-Z]+)*$',
                "Enter a valid service name. Service names can only contain letters, spaces, hyphens, or apostrophes."
    )])
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(1, 'Price cannot be less than 1.')])
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return f'Name: {self.name}'
