from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializer import ShopCartSerializer
from .models import ShoppingCart
# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    '''
    购物车功能开发
    list:获取购物车详情
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    queryset = ShoppingCart.objects.all()