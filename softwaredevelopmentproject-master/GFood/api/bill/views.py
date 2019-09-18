from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.bill.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class BillListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Bill.objects.all()
    serializer_class = BillListSerializer
    permission_classes = (permissions.IsAuthenticated,IsAdmin,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(user = self.request.user)

    def post(self, request):
        serializer = BillCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            cart = Item.objects.filter(bill = None, cart__user= request.user)
            if cart.count() == 0:
                return Response("You have not item to buy", status = status.HTTP_201_CREATED)
            else:
                bill = serializer.save(user = request.user, status="waiting")
                total_price = 0
                for item in cart:
                    total_price += item.price*item.quantity
                    item.bill = bill
                    item.save()
                serializer.save(total = total_price)    
                headers = self.get_success_headers(serializer.data)
                return Response("Add Item successfully", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillListSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
