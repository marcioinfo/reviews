# DJANGO LIBRARY IMPORTS
from django.db import models
from django.utils import timezone
# PROJECT IMPORTS

# DJANGO LIBRARIES IMPORT
from django.dispatch import receiver
from django.db.models.signals import post_save
# PROJECT IMPORTS
#from .models import Blacklist

# DJANGO LIBRARY IMPORTS
from django.db import models
from django.contrib.auth.models import User


# DJANGO LIBRARIES IMPORT
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# PROJECT IMPORTS
#from .models import Profile



class BlacklistManager(models.Manager):
    """ Blacklist Manager

    A manager to execute queries over the Blacklist model.
    """
    @staticmethod
    def erase_expired_tokens():
        """ Erase Expired Tokens

        This query will get all tokens in the blacklist that are expired and
        will delete them from the table.
        """
        Blacklist.objects.filter(expiration__lt=timezone.now()).delete()


class Blacklist(models.Model):
    """ A black list of invalid tokens.

    Tokens that can't be used anymore are stored here.
    """
    token = models.CharField(db_index=True, max_length=1000)
    expiration = models.DateTimeField(db_index=True, null=True)

    objects = BlacklistManager()

    def __str__(self):
        return 'token expires at: ' + str(self.expiration)

    class Meta:
        db_table = 'blacklist'


@receiver(post_save, sender=Blacklist)
def update_blacklist(sender, **kwargs):
    """ Update Blacklist

    Whenever an instance of Blacklist is updated,
    the blacklist table will be updated following the condition:

    Condition - All tokens that are already expired should be deleted
                in order to avoid extra data in the table.
    """
    Blacklist.objects.erase_expired_tokens()



class Profile(models.Model):
    """ This model extends the user.auth standard django model.

    """
    user = models.OneToOneField(User, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(db_index=True, max_length=60, blank=True)
    created = models.DateTimeField(db_index=True, null=True)
    last_modified = models.DateTimeField(db_index=True, null=True)

    def __str__(self):
        return str(self.user) + ' profile'

    class Meta:
        db_table = 'profile'

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
