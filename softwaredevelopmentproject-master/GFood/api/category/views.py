from django.shortcuts import render
from rest_framework import generics, mixins
from GFood.models import *
from GFood.api.category.serializers import *
from rest_framework.response import Response
from rest_framework import status
from GFood.permissions import *
from django_filters.rest_framework import DjangoFilterBackend


class CategoryListView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = (permissions.AllowAny,CanCreateOrNot,)

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)

    def post(self,request):
        # return self.create(request)
        serializer = CategoryCreateSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            self.object = serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response("You was created", status = status.HTTP_201_CREATED, headers = headers)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    def partial_update(self, request, *args, **kwargs):   
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk=None):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return Response("Delete successfully", status = status.HTTP_201_CREATED)
