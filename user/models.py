from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from course.models import Course

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


class Attend(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course,on_delete=models.PROTECT)
    progress = models.DecimalField(max_digits=3,default=0,decimal_places=3)

    
    def __str__(self) -> str:
        return f"{self.user}--{self.course}"

        
