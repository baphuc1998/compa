from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.item.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend

class ItemListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(cart__user=self.request.user)
        #return self.queryset.all()

    def post(self, request):
        serializer = ItemCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            cart = Cart.objects.filter(user = request.user)
            if cart.count() == 1:
                cart = cart.first()
            else:
                cart = Cart.objects.create(user = request.user)
            food_id = request.data['product']
            food = Product.objects.get(id = food_id)
            self.object = serializer.save(cart = cart, price = food.price )
            headers = self.get_success_headers(serializer.data)
            return Response("Add Item successfully", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsItemOwner,)

    def partial_update(self, request, *args, **kwargs):   
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


#part for Merchant's accepting for the bill which was sent by Customer

class MerchantItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = Merchant_ItemListSerializer
    permission_classes = (permissions.IsAuthenticated, IsMerchant,)

    def get_queryset(self):
        return self.queryset.filter(product__restaurant__user=self.request.user)
        # trả về các item mà khách hàng đã order.
        # xử lý: nếu chấp thuận thì trạng thái item đó là completed. Nếu là item đc chấp thuận cuối cùng status bill đó sẽ là delivery.
        # Nếu từ chối thì item đó là rejected. Stripe sẽ hoàn tiền. Tổng bill đc tính toán lại (nên thêm trường Payable vào Bill model).

class MerchantItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = Merchant_ItemDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsProductOwner,)

    def update(self, request, pk= None):
        obj = self.get_object()
        _status = request.data['status']
        if _status == 'cancelled':
            obj.status = 'cancelled'
            obj.save()
            bill = obj.bill
            bill.total = bill.total - (obj.price * obj.quantity)
            bill.save()
        else:
            obj.status = 'delivery'
            obj.save()
        return Response("Change status successfully", status = status.HTTP_201_CREATED)
        
        
