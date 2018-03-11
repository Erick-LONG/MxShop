from .serializers import GoodsSerializer
from .models import Goods
from rest_framework import generics,viewsets,mixins
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class GoodsPagination(PageNumberPagination):
    # 自定义分页
    page_size = 10
    page_size_query_param = 'page_size'# 要多少条数据
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


