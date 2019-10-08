from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class ItemListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_item',lookup_field='pk')
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('cart','bill','price',)
        depth = 2

class ItemCreateSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('cart','bill','price',)

class ItemDetailSerializer(ModelSerializer):
    
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('cart','bill','price','status',)
        depth = 2

class Merchant_ItemListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:merchant_detail_item',lookup_field='pk')

    class Meta:
        model = Item
        fields = '__all__'
        depth = 2

class Merchant_ItemDetailSerializer(ModelSerializer):
    
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('cart','bill','price','quantity','is_deleted',)
        depth = 2


class AdminListItemSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:merchant_detail_item',lookup_field='pk')

    class Meta:
        model = Item
        fields = '__all__'
        depth = 2


class AdminDetailItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('cart','bill','price','quantity',)
        depth = 2


class RevenueSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"
        depth = 2
