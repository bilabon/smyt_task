from django.db import models


class User(models.Model):
    """This is the user model"""

    paycheck = models.IntegerField()
    name = models.CharField(
        max_length=200,
        blank=True)
    date_joined = models.DateTimeField(
        'Date of joining')


class Room(models.Model):
    department = models.CharField(
        max_length=200,
        blank=True)
    spots = models.IntegerField()
