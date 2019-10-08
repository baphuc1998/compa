from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.bill.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import stripe
from GladFood import settings

class BillListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Bill.objects.all()
    serializer_class = BillListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(user = self.request.user)

    def post(self, request):
        serializer = BillCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            cart = Item.objects.filter(bill = None, cart__user= request.user, is_deleted = False)
            if cart.count() == 0:
                return Response("You have not item to buy", status = status.HTTP_201_CREATED)
            if request.user.id_stripe == None:
                return Response("You have not card to buy", status = status.HTTP_200_OK)
            else:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                cus = stripe.Customer.retrieve(
                    request.user.id_stripe
                )
                if not cus.get('sources').get('data'):
                    return Response("You have no anycard to payment for this bill. Please add a card and try again.",status = status.HTTP_201_CREATED)
                bill = serializer.save(user = request.user, status="waiting")
                total_price = 0
                for item in cart:
                    total_price += item.price*item.quantity
                    item.bill = bill
                    item.save()
                try:
                    charge = stripe.Charge.create(
                        amount=total_price,
                        currency='vnd',
                        customer=request.user.id_stripe,
                        #receipt_email='darknessnbp@gmail.com',
                    )
                    bill.id_charge = charge.id
                    bill.save()
                except:
                    return Response("Unexpected Error! Please check your balance and try again.",status = status.HTTP_201_CREATED)
                serializer.save(total = total_price) 
                headers = self.get_success_headers(serializer.data)
                return Response("Add Bill successfully", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BillDetailView(generics.RetrieveDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk=None):
        obj = self.get_object()
        if obj.item_in_bill.filter( Q(status='completed') | Q(status='delivery')).count() > 0:
            return Response("You cannot delete this product because it has been shipped", status=status.HTTP_200_OK)

        for item in obj.item_in_bill.all():
            item.status = "cancelled"
            item.save()
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Refund.create(
                charge=obj.id_charge,
            )
        except:
            return Response("Can not connect to Stripe platform at this time !!", status=status.HTTP_200_OK)
        
        obj.is_deleted = True
        obj.save()
        return Response("Cancel bill successfully", status=status.HTTP_200_OK)
