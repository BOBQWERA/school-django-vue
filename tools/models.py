from django.db import models

# Create your models here.

class Tools(models.Model):
    name = models.CharField(max_length=20)
    urlname = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Files(models.Model):
    name = models.CharField(max_length=100)
    urlname = models.CharField(max_length=100)
    password = models.CharField(max_length=100,null=True,blank=True)
    up_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name