import pytz
from django.db import models
from django.utils import timezone

tz = pytz.timezone('Asia/Shanghai')

# create your models here.


class book(models.Model):
    # 如果没有指定主键的话django会自动新增一个自增id作为主键
    bookname = models.CharField(max_length=128, verbose_name='书名')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.bookname

    def __str__(self):
        return self.bookname

class hostinfo(models.Model):
    hostname = models.CharField(max_length=128,verbose_name='服务器地址')
    port = models.CharField(max_length=128,verbose_name='端口号')
    user = models.CharField(max_length=128, verbose_name='账号')
    password = models.CharField(max_length=128, verbose_name='密码')
    date_time = models.DateTimeField(verbose_name='服务器时间')

    class Meta:
        db_table = 'hostinfo'