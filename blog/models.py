from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from profiles.models import Profile
from django.urls import reverse

User = settings.AUTH_USER_MODEL

# importing datetime module
import datetime

date_time = datetime.date(2021, 5, 8)


class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, null=True, blank=True, editable=False)
    cover = models.URLField(null=True, blank=True, default='https://img-static-s3.s3.us-west-2.amazonaws.com/rough/aaron-burden-y02jEX_B0O0-unsplash.jpg')
    desc = models.TextField()
    date = models.DateField(default=date_time, null=True, blank=True)
    published = models.BooleanField(default=False)
    bookmark = models.ManyToManyField(User, related_name='bookmark', blank=True)
    curate = models.ManyToManyField(User, related_name='curate', blank=True)

    def __str__(self):
        return f"{self.title} | {self.user}"
    