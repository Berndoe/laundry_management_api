from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),

    path('company/', include('catalogue.urls')),
    path('company/', include('catalogue.urls')),

    path('company/', include('orders.urls')),
    path('company/', include('orders.urls')),

    path('company/', include('payments.urls')),

]
