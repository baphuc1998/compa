# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'api.v2/', include('GFood.api_v2.urls')),
    url(r'', include(('GFood.urls','gfood'),namespace='gfood')),

    url(r'^api-auth/', include('rest_framework.urls'))
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)