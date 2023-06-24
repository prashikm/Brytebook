from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings


class Invitation(models.Model):
    email = models.EmailField(null=False, blank=True)
    invitation_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} | {self.code_applied}"


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='profile', default='profile/user.png')

    def __str__(self):
        return self.user.username