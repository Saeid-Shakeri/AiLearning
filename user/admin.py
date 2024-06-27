from django.contrib import admin
from .models import User, ContactUs, Message
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude =('password','groups',)
    search_fields = ['username']


@admin.register(Message)
class Message(admin.ModelAdmin):
    search_fields = ['title']
    exclude = ('reply_date','date')



@admin.register(ContactUs)
class Contact(admin.ModelAdmin):
    search_fields = ['name']
