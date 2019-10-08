from rest_framework import generics
from GFood.permissions import *
from GFood.api.user.serializers import UserDetailSerializer
from rest_framework.response import Response
from GFood.models import CustomUser

class User(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        id = self.request.user.id
        return CustomUser.objects.get(id=id)
    # def retrieve(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = UserDetailSerializer(queryset, many=True)
    #     return Response(serializer.data)
