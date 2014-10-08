from django.db import models


default = '''User:
    doc: This is the user model
    name:
        type: char
        max_length: 200
        blank: false
    date_joined:
        type: date
        args: Date of joining
        blank: false
    paycheck:
        type: int
        blank: false

Room:
    department:
        type: char
        blank: false
        max_length: 200
    spots:
        type: int
        blank: false'''


class Setting(models.Model):
    title = models.TextField('Specifications of Models', default=default)

    class Meta:
        verbose_name_plural = "Setting of Models"

    def __unicode__(self):
        return self.title
