'''
# DJANGO LIBRARIES IMPORT
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# PROJECT IMPORTS
from .models import Profile


# Whenever a New User is created, a new user profile is created as well.
# Whenever a User instance is saved, the user profile instance is saved as
# well. (Last modified is updated)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ This Signal handles the trigger that happens when
    a User.save() signal was sent and/or a User.objects.create_user() is
    called.

    """
    if created:
        Profile.objects.create(user=instance,
                               created=timezone.now(),
                               last_modified=timezone.now(),
                               )

    else:
        profile = Profile.objects.get(user=instance)
        profile.last_modified = timezone.now()
        profile.save()
'''