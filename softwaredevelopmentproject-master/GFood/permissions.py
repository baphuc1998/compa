from rest_framework import permissions
from GFood.models import *
from django.shortcuts import get_object_or_404

class CanRegisterAccount(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous == True:
            return True
        return False

#Only admin can view/post/put/delete
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view,obj):
        return request.user.is_superuser

#Only admin or owner can update/delete account.
# Other user can just view 
class CanUpdateAccount(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_superuser

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser

#Admin can post, the other can just view
class CanCreateOrNot(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

class CanCreateProductOrNot(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.is_merchant

#Only Admin and owner of product can update it
class CanUpdateProduct(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        IsOwner = obj.restaurant == request.user.res_of_user.all().first()
        return IsOwner or request.user.is_superuser

class IsMerchant(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_merchant

class IsProductOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        IsOwner = obj.product.restaurant.user == request.user
        return IsOwner

class IsItemOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        IsOwner = obj.cart.user == request.user
        return IsOwner

class IsReviewOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser

class CanCreateReview(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

class CanApproveReivew(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        IsPossible = obj.product.restaurant.user == request.user
        return IsPossible