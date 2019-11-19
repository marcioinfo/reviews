# DJANGO LIBRARY IMPORTS
from django.db import models
from django.contrib.auth.models import User


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
