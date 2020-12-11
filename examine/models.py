from django.db import models

from user.models import USER_TYPE_CHOICES
# Create your models here.

class Examine(models.Model):
    name = models.CharField(max_length=100)
    tp   = models.CharField(max_length=2,choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.name