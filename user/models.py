from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

cat_choices = (
    ("course", "دوره ها"),
    ("article", "مقاله ها"),
    ("prof", "اساتید"),
    ("lesson", "دروس"),
    ("another", "چیز دیگری"),

)




class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$',
        message="Phone number must be entered in the format: '+989999999999' or '09999999999'. "
    )
    phone = models.CharField(validators=[phone_regex], max_length=14,null=True,blank=True)
    email = models.EmailField(max_length=50,blank=True,null=True,default='')

    def __str__(self) -> str:
        return f"{self.username}"


 



class Message(models.Model):
    title = models.CharField(max_length=50)
    context = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    reply = models.TextField(null=True,blank=True)
    reply_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    category = models.CharField(choices=cat_choices,default="another",max_length=20)

    def __str__(self):
        return f'{self.title}________{self.checked}'
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    


class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    context = models.TextField()
    checked = models.BooleanField(default=False)
    # reply = models.TextField(default='')

    def __str__(self):
        return f'{self.name}________{self.checked}'
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    