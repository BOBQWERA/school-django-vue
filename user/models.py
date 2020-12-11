from django.db import models

from django.utils import timezone

# Create your models here.

USER_TYPE_CHOICES=[
        ('SU','superUser'),
        ('NU','normalUser'),
        ('BL','userInBlackList')
    ]

from examine.models import Examine
class User(models.Model):
    username=models.CharField(max_length=20,unique=True)
    nickname=models.CharField(max_length=20)
    password=models.CharField(max_length=100)
    telephone=models.CharField(max_length=15)
    email=models.EmailField()
    usertype=models.CharField(max_length=2,choices=USER_TYPE_CHOICES)
    credit = models.IntegerField(default=100)
    score = models.IntegerField(default=0)
    face = models.FileField(upload_to='img',null=True,blank=True)
    friend = models.ManyToManyField('self',related_name='friends')
    friend_apply = models.ManyToManyField('self',through='Apply')
    last_logined = models.DateTimeField(auto_now_add=True)
    last_signed  = models.DateTimeField(auto_now_add=True)
    ex = models.ForeignKey(Examine,on_delete=models.CASCADE)

    def __str__(self):
        return self.username

from forum.models import Section

class Visited(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username+'->'+self.section.name+' '

class Apply(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user')
    say = models.CharField(max_length=100)

LIKE_TYPES = [
    ('B','blog'),
    ('P','posting'),
    ('C','comment'),
]


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tp   = models.CharField(max_length=1,choices=LIKE_TYPES)
    to_id = models.IntegerField()

    def __str__(self):
        return self.user.username+':'+self.tp+str(self.to_id)

REPORT_TYPES = [
    ('B','blog'),
    ('P','posting'),
    ('C','comment'),
]

class Report(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tp   = models.CharField(max_length=1,choices=REPORT_TYPES)
    to_id = models.IntegerField()
    num = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username+':'+self.tp+str(self.to_id)