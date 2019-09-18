from django.shortcuts import render
from rest_framework import generics, mixins,viewsets
from GFood.models import *
from GFood.api.merchant.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
#from .permissions import *
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from GladFood import settings
import stripe
from datetime import datetime


class StripeAccountCreateView(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = StripeAccountCreateSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            rules = {
                "rule" : "You must agree to our terms and the 3rd platform"
            }
            return Response(rules, status=status.HTTP_200_OK)
        except:
            return Response("You have no card", status=status.HTTP_200_OK)

    def post(self, request):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            acc = stripe.Account.create(
                type="custom",
                country="US",
                email=request.user.email,
                requested_capabilities=["card_payments", "transfers"],
                business_type="individual",
            )
            merchant = request.user
            merchant.account_stripe = acc.id
            merchant.save()
            return Response("Welcome to members of GladFood", status=status.HTTP_200_OK)
        except:
            return Response("Can not register merchant", status=status.HTTP_400_BAD_REQUEST)
