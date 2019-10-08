from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.item.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import stripe
from GladFood import settings
from django.db.models import Q
import json
from django.core import serializers as sers

class ItemListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,OrderingFilter,)
    filter_fields = ('bill','status',)
    ordering_fields = ['create_at']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(cart__user=self.request.user, is_deleted=False).order_by('-id')
        #return self.queryset.all()

    def post(self, request):
        serializer = ItemCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            try:
                _quantity = request.data['quantity']
                if _quantity < 1:
                    return Response("The quantity is incorrect", status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                return Response("The quantity is incorrect",  status=status.HTTP_406_NOT_ACCEPTABLE)
            cart = Cart.objects.filter(user = request.user)

            if cart.count() == 1:
                cart = cart.first()
            else:
                cart = Cart.objects.create(user = request.user)
            food_id = request.data['product']

            #check item exist?
            item = Item.objects.filter(cart=cart, bill=None, product=food_id, is_deleted=False)
            if item.count() > 0:
                item = item.first()
                item.quantity = request.data['quantity']
                item.save()

                sers_obj = sers.serialize('json', [item,])
                return Response(sers_obj, status = status.HTTP_200_OK)

            food = Product.objects.get(id = food_id)
            self.object = serializer.save(cart = cart, price = food.price )
            headers = self.get_success_headers(serializer.data)
            
            sers_obj = ItemListSerializer(self.object, context={'request': request})

            return Response(sers_obj.data , status = status.HTTP_200_OK, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsItemOwner,)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.bill != None:
            return Response("You can not modify this item because it has already processed")
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk=None):
        obj = self.get_object()
        if obj.bill != None:
            return Response("You can not modify this item because it has already processed")
        obj.is_deleted = True
        obj.save()
        return Response("Delete successfully", status=status.HTTP_200_OK)


#part for Merchant's accepting for the bill which was sent by Customer

class MerchantItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = Merchant_ItemListSerializer
    permission_classes = (permissions.IsAuthenticated, IsMerchant,)
    filter_backends = (DjangoFilterBackend,OrderingFilter,)
    filter_fields = ('status',)
    ordering_fields = ['create_at']

    def get_queryset(self):
        return self.queryset.filter( ~Q(bill=None), product__restaurant__user=self.request.user ).order_by('-id')

class MerchantItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = Merchant_ItemDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsProductOwner,)

    def update(self, request, pk= None):
        obj = self.get_object()
        _status = request.data['status']

        if obj.status == 'completed' or obj.status == 'cancelled':
            return Response("This bill was delivered or cancelled", status = status.HTTP_200_OK)

        if _status == 'delivery':
            obj.status = 'delivery'
            obj.save()
        elif _status == 'completed':
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                item = self.get_object()

                stripe.Transfer.create(
                    amount=int(item.price*item.quantity*0.8*0.00005*100),
                    currency="usd",
                    destination=item.product.restaurant.user.account_stripe,
                    transfer_group="BILL_"+str(item.bill.id)
                )
                obj.status = 'completed'
                obj.save()
                sers_obj = sers.serialize('json', [obj,])

                Response(sers_obj, status = status.HTTP_200_OK)
            except:
                Response("Failed", status = status.HTTP_400_BAD_REQUEST)

        else:
            obj.status = 'cancelled'
            obj.save()
            bill = obj.bill
            bill.total = bill.total - (obj.price * obj.quantity)
            bill.save()
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe.Refund.create(
                    charge=bill.id_charge,
                    amount=(obj.price * obj.quantity)
                )
            except:
                return Response("Can not connect to Stripe platform", status = status.HTTP_200_OK)
        sers_obj = sers.serialize('json', [obj,])
        return Response( sers_obj , status = status.HTTP_200_OK)

from django.db.models import Max, Sum, F, Count
class RevenueAPIView(generics.GenericAPIView):
    
    def get(self, request):
        item = Item.objects.all()
        serializer = RevenueSerializer(item)
        revenue_by_branch = Item.objects.filter(status='completed').values('product__restaurant__name').annotate(Revenue=Sum(F('price')*F('quantity')))
        return Response({'Revenue': revenue_by_branch if revenue_by_branch else 0 })

from itertools import groupby

class Merchant_RevenueAPIView(generics.GenericAPIView):

    def get(self, request):

        invoices = Item.objects.only('create_at', 'price').order_by('create_at')
        month_totals = {
            k: sum(x.price for x in g) 
            for k, g in groupby(invoices, key=lambda i: i.create_at.month)
        }
        return Response(month_totals)
        # _item = Item.objects.filter(status='completed',product__restaurant__user=request.user)
        # revenue = _item.values('product__restaurant__name').annotate(Revenue=Sum(F('price')*F('quantity')))
        # return Response({'Revenue': revenue if revenue else 0 })