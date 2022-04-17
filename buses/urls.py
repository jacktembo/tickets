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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('buses', views.BusViewSet)
router.register('routes', views.RouteViewSet, basename='RouteViewSet')
urlpatterns = [
    path('bus-companies', views.BusCompanies.as_view()),
    path('bus-companies/<int:pk>', views.BusCompanyDetail.as_view()),
    path('tickets', views.Tickets.as_view()),
    path('pay', views.pay),
    path('tickets/<str:pk>', views.TicketDetail.as_view()),
    path('price', views.CalculateTicketPrice.as_view()),
    path('seats', views.Seats.as_view()), # All seats: with their respective status.
    path('tickets-sold/', views.TicketsSold.as_view()), # Using filter backends.
    path('seats-available/<int:route_id>/<departure_date>', views.seats_available),
    path('seats-taken-count/<int:route_id>/<departure_date>', views.number_of_seats_taken),
    path('seats-taken/<int:route_id>/<departure_date>', views.seats_taken),
    path('bus-status/<int:route_id>/<departure_date>', views.is_fully_booked), # Whether a bus is fully booked or not.
    path('seat-status/<int:route_id>/<departure_date>/<int:seat_number>', views.is_seat_available), # Whether a seat is available or booked.
    path('sale-offline/<int:route_id>/<departure_date>/<int:seat_number>', views.sale_offline),
    path('scan/<ticket_number>', views.ScanView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls