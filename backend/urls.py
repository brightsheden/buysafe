
from django.conf.urls.static import  static
from django.conf import settings
from django.contrib import admin
#from django.views.generic import TemplateView 
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('base.urls.auth_urls')),
    path('api/v1/order/', include('base.urls.order_urls')),
     path('api/v1/user/', include('base.urls.user_urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
