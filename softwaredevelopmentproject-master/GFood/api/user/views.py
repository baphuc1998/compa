from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.user.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from Utils import base64Resize
#from .permissions import *
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from GladFood import settings
import stripe

#**********Import************

class UserListView(generics.ListAPIView, mixins.ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    #permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, CanUpdateAccount,)

    def partial_update(self, request, *args, **kwargs):   

        #base64image
        kwargs['partial'] = True
        obj = self.get_object()

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

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny ,CanRegisterAccount,)


class MerchantCreateView(generics.CreateAPIView):
    serializer_class = MerchantCreateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (CanRegisterAccount,)

class ListResetPasswordView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ListUserforAdmin
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    def get_queryset(self):
        return self.queryset.all()
    
class ResetPasswordView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = DetailUserforAdmin
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    
    def update(self,request, pk=None):
        obj = self.get_object()
        password = request.data['password']
        if len(password) > 4: 
            obj.set_password(password)
            obj.save()
            return Response("You have reset password successfully", status = status.HTTP_200_OK)
        return Response("Something went wrong", status = status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView

class ChangePassView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePassSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        oldpwd = request.data['old_password']
        obj = self.request.user
        if obj.check_password(oldpwd):
            newpwd = request.data['new_password']
            obj.set_password(newpwd)
            obj.save()
            return Response("You have changed your password successfully ", status = status.HTTP_200_OK)
        return Response("password incorrect", status = status.HTTP_400_BAD_REQUEST)


#Login API to get token
from rest_framework_simplejwt.views import TokenObtainPairView
class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomObtainTokenSerializer