from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class ReviewListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_review',lookup_field='pk')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','status',)

class ReviewCreateSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','status',)

class ReviewDetailSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','status',)

class Merchant_ReviewListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:merchant_detail_review',lookup_field='pk')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','comment','product','star',)

class Merchant_ReviewDetailSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','comment','product','star',)