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

from . import views, views2
router = DefaultRouter()
router.register('buses', views.BusViewSet)
router.register('routes', views.RouteViewSet, basename='RouteViewSet')

urlpatterns = [
    path('', views2.index, name='index'),
    path('bus-companies', views.BusCompanies.as_view()),
    path('bus-companies/<int:pk>', views.BusCompanyDetail.as_view()),
    path('tickets', views.Tickets.as_view()),
    # path('pay', views.pay),
    # path('pay/confirm', views.pay_confirm),
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
    path('<int:pk>/detail', views2.bus_company_detail, name='bus-company-detail'),
    path('select-seat', views2.mobile_payment, name='select-seat'),
    path('payment-approval', views2.payment_approval, name='payment-approval'),
    path('ticket', views2.ticket, name='ticket'),
    path('<ticket_number>/download', views2.DownloadView.as_view(), name='ticket-download'),
    path('verify-ticket', views2.scan_by_ticket_number, name='verify-by-ticket-number'),
    path('terms', views2.terms, name='terms'),
    path('bus-operator', views2.bus_operator, name='bus-operator'),
    path('<pk>/manage-bus', views2.manage_bus, name='manage-bus'),
    path('<pk>/<int:seat_number>/sale-offline', views2.sale_offline, name='sale-offline'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls