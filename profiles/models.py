from django.db import models
from django.db.models.deletion import CASCADE

from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    bio = models.CharField(max_length=202, blank=False)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name='follow')

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)
    
    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.remove(another_account)

    def __str__(self):
        return self.user.username
