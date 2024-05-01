from django.db import models
from django.core.validators import RegexValidator


class Business(models.Model):
    name = models.CharField(max_length=255, verbose_name="Business Name", help_text="Enter the Business name")
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True, verbose_name="Email",
                              help_text="Enter customer email")
    address = models.TextField(verbose_name="Address", help_text="Enter the Business's address")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    logo = models.ImageField(upload_to='business/')
