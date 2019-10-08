from GFood.models import *
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField

class UserListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:detail_user',lookup_field='pk')

    class Meta:
        model = CustomUser
        fields = ('url','id','username','is_staff','phone','address','is_active')

class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username','password')

    def create(self, validated_data):
        username = validated_data['username']
        # email = validated_data['email']
        password = validated_data['password']

        # user_obj = CustomUser(username = username, email = email)
        user_obj = CustomUser(username=username)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class MerchantCreateSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username','password','email')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user_obj = CustomUser(username = username, email = email, is_merchant= True)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username','name','phone','address', 'image',)
        read_only_fields = ('username',)

class ListUserforAdmin(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='gfood:reset_password',lookup_field='pk')

    class Meta:
        model = CustomUser
        fields = ('id','url','username','password')

class DetailUserforAdmin(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id','name','username','password')
        read_only_fields = ('name','username',)
        extra_kwargs = {'password': {'write_only': True}}

    # def update(self, instance, validated_data):
    #     password = validated_data.get('password', instance.password)
    #     instance.set_password(password)
    #     instance.save()
    #     return instance

class ResetPassword_S(ModelSerializer):
    #password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('username','password','email')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class ChangePassSerializer(ModelSerializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('old_password','new_password')

    # def create(self, validated_data):
    #     oldpwd = validated_data['old_password']
    #     newpwd = validated_data['new_password']
    #     if self.request.user.password.check_password(oldpwd):
    #         print(self.request.user.password.check_password(oldpwd))
    #     return validated_data


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomObtainTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.is_superuser:
            token['type'] = 'admin'
        elif user.is_merchant:
            token['type'] = 'merchant'
        else:
            token['type'] = 'customer'
        return token