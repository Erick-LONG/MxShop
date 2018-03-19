from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from user_operation.models import UserFav

User = get_user_model()

#利用信号机制
@receiver(post_save,sender=UserFav)
def create_userfav(sender,instance=None,created = False,**kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

#利用信号机制
@receiver(post_delete,sender=UserFav)
def create_userfav(sender,instance=None,created = False,**kwargs):
    if created:
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()