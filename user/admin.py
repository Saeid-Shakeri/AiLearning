from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class Userdmin(admin.ModelAdmin):
    search_fields = ['username']
