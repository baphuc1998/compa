from django.shortcuts import render
from rest_framework import generics, mixins,viewsets
from GFood.models import *
from GFood.api.card.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
#from .permissions import *
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from GladFood import settings
import stripe
from datetime import datetime

def check(month, year):
    d = datetime.today()
    if year > d.year and month<=12:
        return True
    elif year == d.year and (month-d.year) > 2 and month<=12 :
        return True
    else:
        return False


class CardCreateView(generics.CreateAPIView):
    serializer_class = CardCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            cards = stripe.Customer.list_sources(
                request.user.id_stripe,
                limit=2,
                object='card'
            )

            if len(cards['data']) > 0:
                return Response("Your card already exists", status=status.HTTP_200_OK)
            serializer = CardCreateSerializer(data=request.data)
            if serializer.is_valid():
                card_number = serializer.validated_data['card_number']
                exp_month = serializer.validated_data['exp_month']
                exp_year = serializer.validated_data['exp_year']
                cvc = serializer.validated_data['cvc']

                if not check(exp_month, exp_year):
                    return Response("This card has expired or is about to expire soon", status=status.HTTP_200_OK)

                if request.user.id_stripe == None:
                    user = request.user
                    new_stripe = stripe.Customer.create(
                        description="Customer for "+user.username,
                        #source="tok_mastercard",
                        email=user.email
                    )

                    user.id_stripe = new_stripe.id
                    user.save()

                    token = stripe.Token.create(
                        card={
                            'number': card_number,
                            'exp_month': exp_month,
                            'exp_year': exp_year,
                            'cvc': cvc,
                        }
                    )
                    card = stripe.Customer.create_source(
                        user.id_stripe,
                        source=token.id
                    )
                    print(token)
                    print(card)
                else:
                    token = stripe.Token.create(
                        card={
                            'number': card_number,
                            'exp_month': exp_month,
                            'exp_year': exp_year,
                            'cvc': cvc,
                        }
                    )
                    card = stripe.Customer.create_source(
                        self.request.user.id_stripe,
                        source=token.id
                    )
                    print(token)
                    print(card)
                return Response("Create card successful.", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Can not connect to Stripe at this time !!", status=status.HTTP_400_BAD_REQUEST)

class CardDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            cards = stripe.Customer.list_sources(
                request.user.id_stripe,
                limit=2,
                object='card'
            )
            mycard = cards['data'][0]
            card = {
                    'number': "*****"+mycard['last4'],
                    'exp_month': mycard['exp_month'],
                    'exp_year': mycard['exp_year'],
                    'brand': mycard['brand'],
            }
            return Response(card, status=status.HTTP_200_OK)
        except:
            return Response("You have no card", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            cards = stripe.Customer.list_sources(
                request.user.id_stripe,
                limit=2,
                object='card'
            )
            mycard = cards['data'][0]
            print(mycard.id)
            stripe.Customer.delete_source(
                request.user.id_stripe,
                mycard.id
            )

            return Response("Delete Successfully", status=status.HTTP_200_OK)
        except:
            return Response("You have no card", status=status.HTTP_200_OK)
