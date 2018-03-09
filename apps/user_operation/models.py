from datetime import datetime
from django.db import models

from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model() #返回User类


# Create your models here.
class UserFav(models.Model):
    '''用户收藏'''
    user = models.ForeignKey(User,verbose_name='用户')
    goods = models.ForeignKey(Goods,verbose_name='商品')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserLeavingMessage(models.Model):
    '''用户留言'''

    MESSAGE_CHOICE=(
        (1,'留言'),
        (2,'投诉'),
        (3,'询问'),
        (4,'售后'),
        (5,'求购'),
    )
    user = models.ForeignKey(User,verbose_name='用户')
    msg_type = models.IntegerField(default=1,choices=MESSAGE_CHOICE,verbose_name='留言类型',
                                   help_text='留言类型：1(留言),2(投诉),3(询问),4(售后),5(求购)')
    subject = models.CharField(max_length=100,verbose_name='主题',default='')
    message = models.TextField(default='',verbose_name='留言内容',help_text='留言内容')
    file = models.FileField(verbose_name='上传文件',help_text='上传文件')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    '''用户收货地址'''
    user = models.ForeignKey(User,verbose_name='用户')
    district = models.CharField(max_length=100,verbose_name='区域',default='')
    address = models.CharField(max_length=100,verbose_name='详细地址',default='')
    signer_mobile = models.CharField(max_length=100,verbose_name='电话',default='')
    signer_name = models.CharField(max_length=100,verbose_name='签收人',default='')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address