from django.db import models

# Create your models here.
class People(models.Model):
    Pno = models.CharField( primary_key=True,max_length=50)
    Password = models.CharField(max_length=50)
    Page = models.IntegerField(default='20')
    Psex = models.CharField(max_length=10,default='man')
    #isdownload = models.CharField(max_length=5,default='2')#判断文件是否在下载，1在下载，2，没在下载
'''class People(models.Model):
    Pno = models.CharField(primary_key=True,max_length=50)
    filename = models.CharField(max_length=200)
    '''
    
