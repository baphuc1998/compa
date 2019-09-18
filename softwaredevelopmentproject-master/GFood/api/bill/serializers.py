from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class BillListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_bill',lookup_field='pk')

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('user','total','is_deleted','status',)

class BillCreateSerializer(ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('user','total','is_deleted','status',)

class BillDetailSerializer(ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('user','total','is_deleted','address',)


class Merchant_BillListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:merchant_detail_bill',lookup_field='pk')

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('user','total','status',)