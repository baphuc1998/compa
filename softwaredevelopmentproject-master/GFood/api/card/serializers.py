from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class CardCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    exp_month = serializers.IntegerField()
    exp_year = serializers.IntegerField()
    cvc = serializers.CharField(max_length=3)

class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'