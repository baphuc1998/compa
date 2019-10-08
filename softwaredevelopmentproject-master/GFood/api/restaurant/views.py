from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.restaurant.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from Utils import base64Resize
from GladFood import settings

class RestaurantListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False).order_by('-id')

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


        serializer = RestaurantCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.object = serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            sers_obj = RestaurantListSerializer(self.object, context={'request': request})
            return Response( sers_obj.data , status=status.HTTP_200_OK, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # self.object = serializer.save()
        # return self.create(request)
        # if serializer.is_valid():
        #     self.object = serializer.save()
        #     headers = self.get_success_headers(serializer.data)
        #     # Here we serialize the object with the proper depth = 2
        #     new_c = ProgramGet(self.object, context={'request': request})
        #     return Response(new_c.data, status = status.HTTP_200_OK, headers = headers)
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = (permissions.AllowAny, IsOwnerOrAdmin,)

    # def update(self, request, pk=None):
    #     obj = self.get_object()
    #     obj.user=self.request.user
    #     obj.save()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.user = self.request.user
        obj.save()
        return self.update(request, *args, **kwargs)

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
        return Response("Delete successfully", status=status.HTTP_200_OK)


# Part only for admin

class ListApprovalView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = ListApprovedSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_active',)

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class DetailApprovalView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = ApprovedSerializer
    permission_classes = (IsAdmin,)

    # def update(self,request, pk=None):
    #     obj = self.get_object()
    #     is_active = request.data['is_active']
    #     if is_active:
    #         if is_active == 'true':
    #             obj.is_active = True
    #             obj.save()
    #             obj_user = obj.user
    #             obj_user.is_merchant = True
    #             obj_user.save()
    #             return Response("Successfully", status = status.HTTP_200_OK)
    #         else:
    #             obj.is_active = False
    #             obj.save()
    #             obj_user = obj.user
    #             obj_user.is_merchant = False
    #             obj_user.save()
    #             return Response("Successfully", status = status.HTTP_200_OK)
    #     else:
    #         return Response("Something went wrong", status = status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        obj = self.get_object()
        is_active = request.data['is_active']
        if is_active:
            if is_active == 'True' or is_active == 'true':
                obj.is_active = True
                obj.save()
                obj_user = obj.user
                obj_user.is_merchant = True
                obj_user.save()
                return Response("Active Successfully", status = status.HTTP_200_OK)
            else:
                obj.is_active = False
                obj.save()
                obj_user = obj.user
                obj_user.is_merchant = False
                obj_user.save()
                return Response("Deactive Successfully", status = status.HTTP_200_OK)
        else:
            return Response("Something went wrong", status = status.HTTP_400_BAD_REQUEST)

        return self.update(request, *args, **kwargs)
