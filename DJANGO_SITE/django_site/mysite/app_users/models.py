from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    class Meta:
        db_table = 'profile'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ['city']

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    customer_id = models.CharField(max_length=40)

