from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField


class ProductListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_product',lookup_field='pk')

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('restaurant','is_deleted','status',)

class ProductCreateSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('restaurant','is_deleted','status',)

class ProductDetailSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        depth = 2
        read_only_fields = ('restaurant','is_deleted',)