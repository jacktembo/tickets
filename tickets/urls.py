"""tickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

admin.AdminSite.site_header = 'All1Zed Bus Ticketing System'
admin.AdminSite.site_title = 'All1Zed Bus Tickets'
admin.AdminSite.index_title = 'Greetings From All1Zed! Welcome To The Secure Bus Ticket Portal. How Are You Today?'
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('buses.urls')),
    path('', include('internal.urls')),
    path('api/', include('buses.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('bulk-routes', views.BulkRoutesUpload.as_view(), name='bulk-routes'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
