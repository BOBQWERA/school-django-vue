from django.db import models

from user.models import User
from examine.models import Examine
# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    headline = models.CharField(max_length=50)
    text = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    hits = models.IntegerField(default=0)
    number_of_likes = models.IntegerField(default=0)
    share = models.BooleanField(default=False)
    abstract = models.CharField(max_length=100,default='暂无简介，进来看看吧')
    ex = models.ForeignKey(Examine,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']

    def __str__(self):
        return self.headline+'--'+self.author.username
