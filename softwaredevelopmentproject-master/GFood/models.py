from django.db import models
from django.contrib.auth.models import AbstractUser
# from model_utils import Choices

class CustomUser(AbstractUser):
    # username to login
    # name to display profile
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100)
    image = models.TextField()
    id_stripe = models.CharField(max_length=100, null=True)
    # if user sign out, remember delete token
    token_fcm = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    # manage store
    is_vip = models.BooleanField(default=False)
    # is seller
    is_merchant = models.BooleanField(default=False)
    # delete account
    is_deleted = models.BooleanField(default=False)
    account_stripe = models.CharField(max_length=30, null=True)
    
    # def __str__(self):
    #     return str(self.name)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
    image = models.TextField()
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='res_of_user', null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    detail = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.TextField()
    category = models.ManyToManyField(
        Category, related_name='product_in_category', null=True)
    restaurant = models.ForeignKey(
        Restaurant, related_name='product_in_res', on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)
    #_Choices = Choices('Out of stock','In stock')
    #status = models.CharField(max_length=50 ,default='In stock',null=True, choices=_Choices)
    status = models.CharField(max_length=50, default='In stock', null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name='cart_of_user', on_delete=models.CASCADE, primary_key=True)
    # sum price of all products
    total = models.IntegerField(null=True)

class Bill(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='bill_of_user', null=True)
    total = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now=True, null=True)

    #_Choices = Choices('waiting', 'checking', 'delivery','completed','cancelled')
    #status = models.CharField(max_length=15,null=True, choices=_Choices)
    status = models.CharField(max_length=15,null=True)
    address = models.CharField(max_length=100, null=True)
    is_deleted = models.BooleanField(default=False, null=True)

class Item(models.Model):
    product = models.ForeignKey(
        Product, related_name='item_in_product', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    cart = models.ForeignKey(
        Cart, related_name='item_in_cart', on_delete=models.CASCADE, null=True)
    bill = models.ForeignKey(
        Bill, related_name='item_in_bill', on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now=True)
    #_Choices = Choices('waiting', 'checking', 'delivery','completed','cancelled')
    #status = models.CharField(max_length=15,choices=_Choices,null=True, default='waiting')
    status = models.CharField(max_length=15, null=True, default='waiting')

class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='review_of_user', null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name='review_of_product', null=True)
    # vote star for product
    star = models.IntegerField(null=True)
    comment = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
