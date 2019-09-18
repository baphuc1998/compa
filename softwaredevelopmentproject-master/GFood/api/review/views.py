from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.review.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend


class ReviewListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return self.queryset.all()

    def post(self, request):
        serializer = ReviewCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            self.object = serializer.save(user = request.user)
            headers = self.get_success_headers(serializer.data)
            return Response("Add review successfully", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsReviewOwner,)

    # def put(self, request, *args, **kwargs):
    #     rs = self.partial_update(request, *args, **kwargs)
    #     print('*******',rs)
    #     return Response(status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):   
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     print(serializer)
    #     return Response(status=status.HTTP_202_ACCEPTED)

class MerchantReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = Merchant_ReviewListSerializer
    permission_classes = (permissions.IsAuthenticated,IsMerchant,)

    def get_queryset(self):
        return self.queryset.filter(product__restaurant__user=self.request.user)

class MerchantReviewDetailView(generics.RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = Merchant_ReviewDetailSerializer
    permission_classes = (permissions.IsAuthenticated,CanApproveReivew,)