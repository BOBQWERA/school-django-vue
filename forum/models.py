from django.db import models

from user.models import User
from tools.models import Files
# Create your models here.

USER_TYPE_CHOICES=[
        ('SU','superUser'),
        ('NU','normalUser'),
        ('BL','userInBlackList')
    ]

class Forum(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

from examine.models import Examine
class Section(models.Model):
    name = models.CharField(max_length=30)
    allow_groups = models.CharField(max_length=10) #split with space
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)
    urlname = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Posting(models.Model):
    landlord = models.ForeignKey(User,on_delete=models.CASCADE)
    headline = models.CharField(max_length=30)
    text = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    floor = models.IntegerField(default=1)
    ex = models.ForeignKey(Examine,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time']

    def __str__(self):
        return self.headline

class Comment(models.Model):
    publisher = models.ForeignKey(User,on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting,on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    floor = models.IntegerField()
    append_file = models.ForeignKey(Files,on_delete=models.CASCADE,blank=True,null=True)
    ex = models.ForeignKey(Examine,on_delete=models.CASCADE)

    def __str__(self):
        return self.content