"""tickets buses URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('passenger/', views.Passenger.as_view()),
    path('', views.Buses.as_view()),
    path('<int:pk>', views.BusDetail.as_view()),
    path('routes/', views.Routes.as_view()),
    path('routes/<int:pk>', views.RouteDetail.as_view()),
    path('tickets/', views.Tickets.as_view()),
    path('tickets/<int:pk>', views.TicketDetail.as_view()),
    path('price/<str:bus_short_name>/<int:route_id>', views.calculate_ticket_price),
    path('routes/<str:bus_short_name>/', views.find_bus_routes),
    path('<str:bus_short_name>/times', views.find_departure_times),
]
