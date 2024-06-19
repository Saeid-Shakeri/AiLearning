from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$',
        message="Phone number must be entered in the format: '+989999999999' or '09999999999'. "
    )
    phone = models.CharField(validators=[phone_regex], max_length=14)
    email = models.EmailField(max_length=50,blank=True,null=True,default='')

    def __str__(self) -> str:
        return f"{self.username}"


        

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    context = models.TextField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
    