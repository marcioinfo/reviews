# DJANGO LIBRARIES IMPORT
from django.dispatch import receiver
from django.db.models.signals import post_save
# PROJECT IMPORTS
from .models import Blacklist


@receiver(post_save, sender=Blacklist)
def update_blacklist(sender, **kwargs):
    """ Update Blacklist

    Whenever an instance of Blacklist is updated,
    the blacklist table will be updated following the condition:

    Condition - All tokens that are already expired should be deleted
                in order to avoid extra data in the table.
    """
    Blacklist.objects.erase_expired_tokens()
