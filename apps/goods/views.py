from .serializers import GoodsSerializer,CategorySerializer,BannerSerializer
from .models import Goods,GoodsCategory,Banner
from rest_framework import generics,viewsets,mixins,filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
# Create your views here.


class GoodsPagination(PageNumberPagination):
    # 自定义分页
    page_size = 12
    page_size_query_param = 'page_size'# 要多少条数据
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    商品列表页,分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all().order_by('-add_time')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    #authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')


class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = []
    serializer_class = ''


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer

