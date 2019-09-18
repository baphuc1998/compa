from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class CategoryListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_category',lookup_field='pk')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('create_at', 'is_deleted',)

class CategoryCreateSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('create_at', 'is_deleted',)

class CategoryDetailSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('name','detail')