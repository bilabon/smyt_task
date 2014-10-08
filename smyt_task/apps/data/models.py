from django.db import models


class User(models.Model):
    """This is the user model"""

    paycheck = models.IntegerField(
        blank=False)
    name = models.CharField(
        max_length=200,
        blank=False)
    date_joined = models.DateField(
        'Date of joining',
        blank=False)


class Room(models.Model):
    department = models.CharField(
        max_length=200,
        blank=False)
    spots = models.IntegerField(
        blank=False)
