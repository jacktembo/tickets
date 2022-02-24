"""tickets buses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Addhttps://www.yoquutube.com/ an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import DefaultRouter

router = DefaultRouter()
router.register('buses', views.BusViewSet)
router.register('routes', views.RouteViewSet)
router.register('times', views.DepartureTimes, basename='times')
urlpatterns = [
    path('bus-companies', views.BusCompanies.as_view()),
    path('bus-companies/<int:pk>', views.BusCompanyDetail.as_view()),
    path('tickets', views.Tickets.as_view()),
    path('tickets/<str:pk>', views.TicketDetail.as_view()),
    path('price', views.CalculateTicketPrice.as_view()),
    path('routes', views.BusRoutes.as_view()),
    path('tickets-sold/', views.TicketsSold.as_view()),
    path('seats-available', views.SeatsAvailable.as_view())

]
urlpatterns += router.urls