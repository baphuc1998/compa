from django.conf.urls import url, include


urlpatterns = [
    url(r'^server/', include('GFood.api_v2.server.urls')),
    url(r'^user/', include('GFood.api_v2.user.urls')),
    url(r'^item/', include('GFood.api_v2.item.urls')),
]