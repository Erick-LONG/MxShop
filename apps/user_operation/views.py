from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from .serializer import UserFavSerializer
from .models import UserFav,UserLeavingMessage
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializer import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer


class UserFavViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏列表功能
    retrieve：
        判断某个商品是否已经收藏
    create：
        收藏商品
    '''
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user = self.request.user)

    def get_serializer_class(self):
        #自定义获取用户收藏详情和添加删除收藏
        if self.action =='list':
            return UserFavDetailSerializer
        elif self.action =='create':
            return UserFavSerializer
        return UserFavSerializer


class LeavingMessageViewSet(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    '''
    list:
        获取用户留言
    create：
        添加用户留言
    destroy：
        删除用户留言
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects .filter(user = self.request.user)