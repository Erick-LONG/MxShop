from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

#利用信号机制，密码保存为密文
@receiver(post_save,sender=User)
def create_user(sender,instance=None,created = False,**kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()