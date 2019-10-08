from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .api.user import views as user_views
from .api.bill import views as bill_views
from .api.cart import views as cart_views
from .api.category import views as category_views
from .api.product import views as product_views
from .api.restaurant import views as restaurant_views
from .api.review import views as review_views
from .api.item import views as item_views
from .api.card import views as card_views
from .api.merchant import views as merchant_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #login to generate token
    url(r'^api/user/login/$', user_views.LoginAPIView.as_view() ),
    #url(r'^api/user/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/user/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),

    #merchant api
    url(r'^api/merchant/rules/$', merchant_views.StripeAccountCreateView.as_view() ),

    #user api
    url(r'^api/user/$', user_views.UserListView.as_view(), name='list_user' ),
    url(r'^api/user/(?P<pk>\d+)/$', user_views.UserDetailView.as_view(), name='detail_user' ),
    #url(r'^api/user/register/$', user_views.UserCreateView.as_view()),
    url(r'^api/user/register/$', user_views.UserCreateView.as_view()),
    url(r'^api/merchant/register/$', user_views.MerchantCreateView.as_view() ),
    
    url(r'^api/user/changepwd/$', user_views.ChangePassView.as_view() ),
    #set password api
    url(r'^api/admin/user/$', user_views.ListResetPasswordView.as_view(), name='list_reset'),
    url(r'^api/admin/user/(?P<pk>\d+)/$', user_views.ResetPasswordView.as_view() , name='reset_password'),

    #restaurant api
    url(r'^api/restaurant/$', restaurant_views.RestaurantListView.as_view(), name='list_restaurant' ),
    url(r'^api/restaurant/(?P<pk>\d+)/$', restaurant_views.RestaurantDetailView.as_view(), name='detail_restaurant' ),

    #admin api
    url(r'^api/admin/restaurant/$', restaurant_views.ListApprovalView.as_view(), name='list_approval_restaurant' ),
    url(r'^api/admin/restaurant/(?P<pk>\d+)/$', restaurant_views.DetailApprovalView.as_view(), name='detail_approval_restaurant'),

    #category api
    url(r'^api/category/$', category_views.CategoryListView.as_view(), name='list_category'),
    url(r'^api/category/(?P<pk>\d+)', category_views.CategoryDetailView.as_view(), name='detail_category'),

    #product api
    url(r'^api/product/$', product_views.ProductListView.as_view(), name='list_product'),
    url(r'^api/product/(?P<pk>\d+)', product_views.ProductDetailView.as_view(), name='detail_product' ),

    #item api
    url(r'^api/item/$', item_views.ItemListView.as_view(), name='list_item'),
    url(r'^api/item/(?P<pk>\d+)', item_views.ItemDetailView.as_view(), name='detail_item' ),
    url(r'^api/merchant/item/$', item_views.MerchantItemListView.as_view(), name='merchant_list_item'), #List item for merchant accept.
    url(r'^api/merchant/item/(?P<pk>\d+)', item_views.MerchantItemDetailView.as_view(), name='merchant_detail_item'),

    #cart api
    url(r'^api/cart/$', cart_views.CartListView.as_view(), name='list_cart'),
    #url(r'^api/ca/(?P<pk>\d+)', item_views.ItemDetailView.as_view(), name='detail_item' ),

    #bill api
    url(r'^api/bill/$', bill_views.BillListView.as_view(), name='list_bill'),
    url(r'^api/bill/(?P<pk>\d+)', bill_views.BillDetailView.as_view(), name='detail_bill' ),

    #review api
    url(r'^api/review/$', review_views.ReviewListView.as_view(), name='list_review'),
    url(r'^api/review/(?P<pk>\d+)', review_views.ReviewDetailView.as_view(), name='detail_review'),
    url(r'^api/merchant/review/$', review_views.MerchantReviewListView.as_view(), name='merchant_list_review'),
    url(r'^api/merchant/review/(?P<pk>\d+)', review_views.MerchantReviewDetailView.as_view(), name='merchant_detail_review'),

    #card api
    url(r'^api/user/card/$', card_views.CardCreateView.as_view() ),
    url(r'^api/user/mycard/$', card_views.CardDetailView.as_view() ),

    #Revenue API
    url(r'^api/revenue/$', item_views.RevenueAPIView.as_view() ),
    url(r'^api/merchant/revenue/$', item_views.Merchant_RevenueAPIView.as_view() ),


]
