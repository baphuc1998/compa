from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class RestaurantListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_restaurant',lookup_field='pk')

    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 2
        read_only_fields = ('is_active','is_deleted',)

class RestaurantCreateSerializer(ModelSerializer):
    
    class Meta:
        model = Restaurant
        fields= '__all__'
        read_only_fields = ('is_active','is_deleted',)

class RestaurantDetailSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 2
        read_only_fields = ('is_active','is_deleted',)

class ListApprovedSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_approval_restaurant',lookup_field='pk')

    class Meta:
        model = Restaurant
        fields = ('id','name','url','is_active','image')

class ApprovedSerializer(ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id','name','is_active','image')
        read_only_fields = ('name','image',)