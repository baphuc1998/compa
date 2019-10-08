from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.cart.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class CartListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = CartListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(bill=None, cart__user=self.request.user, is_deleted=False)