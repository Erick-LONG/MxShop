from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from .serializers import SmsSerializer,UserRegSerializer
from rest_framework.response import Response
from rest_framework import status
from MxShop.settings import API_KEY
from random import choice
from .models import VerifyCode

from utils.yunpian_sms import Yunpian

User = get_user_model()
# Create your views here.


class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''

    def authenticate(self,username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin,viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        '''生成四位数据验证码'''
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        '''发送短信验证码'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        #云片网接口发送短信
        yunpian = Yunpian(API_KEY)
        code = self.generate_code()
        sms_status = yunpian.send_sms(code=code,mobile=mobile)

        #判断短信发送状态
        if sms_status['code'] !=0:
            return Response({
                'mobile':sms_status['msg'],
            },status.HTTP_400_BAD_REQUEST)
        else:

            #如果发送成功，保存到数据库，并返回状态码
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({'mobile':mobile},status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin,viewsets.GenericViewSet):
    '''用户'''
    serializer_class = UserRegSerializer

