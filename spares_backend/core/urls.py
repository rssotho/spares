from django.contrib import admin
from django.urls import (
    path,
    include
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('spares_api/system_management/', include('system_management.urls')),
    path('spares_api/product_management/', include('product_management.urls')),
]
