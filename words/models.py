from django.db import models

from user.models import User
# Create your models here.

class WordData(models.Model):
    word = models.CharField(max_length=40)
    translate = models.CharField(max_length=100)
    groop = models.CharField(max_length=10)
    md5   = models.CharField(max_length=50,default=None,null=True)

    class Meta:
        ordering = ['md5']

    def __str__(self):
        return '['+self.word +' '+ self.groop+']'

class WordPlan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateField(auto_created=True)
    groop      = models.CharField(max_length=10)
    num = models.IntegerField()
    index = models.IntegerField(default=0)

    def __str__(self):
        return '['+self.user.username+' '+self.groop+' '+str(self.num)+']'