from django.db import models

# Create your models here.

IMAGE_TYPE_CHOICES = [
    ('jpg','.jpg'),
    ('png','.png'),
    ('gif','.gif'),
    ('bmp','.bmp'),
    ('jpeg','.jpeg')
]


class Imagedata(models.Model):
    name = models.CharField(max_length=30)
    tp   = models.CharField(max_length=4,choices=IMAGE_TYPE_CHOICES)
    origin_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/')
    