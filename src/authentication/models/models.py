# DJANGO LIBRARY IMPORTS
from django.db import models
from django.utils import timezone
# PROJECT IMPORTS




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
