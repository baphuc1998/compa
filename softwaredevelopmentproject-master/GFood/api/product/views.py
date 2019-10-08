from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.product.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from GFood.patigations import *
from GladFood import settings
from Utils import base64Resize

class ProductListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CanCreateProductOrNot,)
#     pagination_class = Patigation_50_item

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('restaurant',)

    def get_queryset(self):
        # return self.queryset.filter(is_deleted=False, restaurant__is_active=True).order_by("?")
        return self.queryset.filter(is_deleted=False, restaurant__is_active=True).order_by('-id')

    def post(self, request):
        # base64image
        try:
            str_image = request.data['image']
            # print(str_image)
            request.data['image'] = base64Resize.resize(str_image)
        except:
            try:
                request.data['image'] = settings.MEDIA_URL + '/' + 'images.png'
            except:
                pass


        serializer = ProductCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            restaurant = self.request.user.res_of_user.all().first()
            self.object = serializer.save(restaurant = restaurant)
            headers = self.get_success_headers(serializer.data)
            return Response("Create successfully", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CanUpdateProduct,)

    def partial_update(self, request, *args, **kwargs):   
        # kwargs['partial'] = True
        # return self.update(request, *args, **kwargs)

        # base64image
        kwargs['partial'] = True

        try:
            str_image = request.data['image']
            # print(str_image)
            request.data['image'] = base64Resize.resize(str_image)
        except:
            try:
                obj = self.get_object()
                request.data['image'] = obj.image
            except:
                try:
                    request.data['image'] = settings.MEDIA_URL + '/' + 'images.png'
                except:
                    pass
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk=None):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return Response("Delete successfully", status = status.HTTP_201_CREATED)
