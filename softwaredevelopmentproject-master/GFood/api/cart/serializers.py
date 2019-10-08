from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class CartListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_item',lookup_field='pk')

    class Meta:
        model = Item
        fields = '__all__'
        #read_only_fields = ('create_at', 'is_deleted',)
        depth = 2

class CartCreateSerializer(ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        #read_only_fields = ('create_at', 'is_deleted',)

class CartDetailSerializer(ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        depth = 2 