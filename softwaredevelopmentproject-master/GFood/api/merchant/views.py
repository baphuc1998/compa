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
    permission_classes = (permissions.IsAuthenticated, IsMerchant, )

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            rules = {
                "rule" : "You must agree to our terms and the 3rd platform. Accepting this agreement helps you to getting benefit from your business."
            }
            return Response(rules, status=status.HTTP_200_OK)
        except:
            return Response("You have no card", status=status.HTTP_200_OK)

    def post(self, request):
        #print(request.user.account_stripe)
        if request.user.account_stripe != None:
            return Response("You are already a member in GFood", status=status.HTTP_200_OK)
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            acc = stripe.Account.create(
                type="custom",
                country="US",
                email=str(request.user.username)+"@gmail.com",
                requested_capabilities=["card_payments", "transfers"],
                business_type="individual",
            )
            merchant = request.user
            merchant.account_stripe = acc.id
            merchant.save()
            return Response("Welcome to  be a member of GladFood ! Thank you very much", status=status.HTTP_200_OK)
        except:
            return Response("Can not register merchant", status=status.HTTP_400_BAD_REQUEST)
