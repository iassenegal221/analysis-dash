# myproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp.views import dash_view, dash_ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dash/', dash_view, name='dash_view'),
    path('dash_ajax/', dash_ajax, name='dash_ajax'),
]
