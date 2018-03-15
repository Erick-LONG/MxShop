from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets,mixins,authentication
from rest_framework.permissions import IsAuthenticated
from .serializers import SmsSerializer,UserRegSerializer,UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from MxShop.settings import API_KEY
from random import choice
from .models import VerifyCode
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

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


class UserViewSet(CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''用户'''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)

    def get_serializer_class(self):
        #自定义获取详情和注册用户的序列化类
        if self.action =='retrieve':
            return UserDetailSerializer
        elif self.action =='create':
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action=='retrieve':
            return [IsAuthenticated()]
        elif self.action =='create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    #返回当前用户，用于获取当前用户详情
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        serializer.save()

