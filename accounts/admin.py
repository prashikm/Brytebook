from django.contrib import admin
from .models import CustomUser, Invitation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'custom_user'


class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserInline)


# Register your models here.
admin.site.register(Invitation)
admin.site.register(CustomUser)