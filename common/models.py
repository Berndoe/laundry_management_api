from django.db import models


class BaseModel(models.Model):
    """
    This model is defined for common properties of all models
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
