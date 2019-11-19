from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):

    rating = models.IntegerField(validators=[MaxValueValidator(5),
                                             MinValueValidator(1)])

    title = models.CharField(max_length=64)

    summary = models.CharField(max_length=10000)

    # max length based on IPv4-mapped IPv6 (45 chars):
    # ABCD:ABCD:ABCD:ABCD:ABCD:ABCD:XXX.XXX.XXX.XXX
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    submission_date = models.DateTimeField(auto_now_add=True,
                                           blank=True,
                                           null=True)

    company_name = models.CharField(max_length=100)

    reviewer = models.ForeignKey('registration.Profile',
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'
