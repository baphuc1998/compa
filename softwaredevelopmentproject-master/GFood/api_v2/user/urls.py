from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.User.as_view()),
]