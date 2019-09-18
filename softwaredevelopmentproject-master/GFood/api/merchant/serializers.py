from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField


class StripeAccountCreateSerializer(serializers.Serializer):
    agreement = serializers.BooleanField()