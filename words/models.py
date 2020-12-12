from django.db import models

# Create your models here.

class WordData(models.Model):
    word = models.CharField(max_length=40)
    translate = models.CharField(max_length=100)
    groop = models.CharField(max_length=10)

    def __str__(self):
        return '['+self.word +' '+ self.groop+']'