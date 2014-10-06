from django.db import models


default = '''User:
    doc: This is the user model
    name:
        type: char
        max_length: 200
    date_joined:
        type: datetime
        args: Date of joining
    paycheck:
        type: int

Room:
    department:
        type: char
        max_length: 200
    spots:
        type: int'''


class Setting(models.Model):
    title = models.TextField('View of Models', default=default)

    class Meta:
        verbose_name_plural = "Setting of models"

    def __unicode__(self):
        return self.title
