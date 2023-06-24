from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile, Following
from django.contrib.auth.models import User
from .models import CustomUser
# from django.core.mail import send_mail

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Following.objects.create(user=instance)
        CustomUser.objects.create(user=instance)

        # email = instance.email
        # print(email)

        # send_mail(
        #     'Successfully created Brytebook account',
        #     'Welcome to Brytebook',
        #     'prashikm861@gmail.com',
        #     ['to@example.com'],
        #     fail_silently=False,
        # )
        # 1b003782-495c-4515-a1a1-124312b8c33e