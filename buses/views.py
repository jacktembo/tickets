import dbus.service
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.routers import DefaultRouter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .models import *
from .serializers import *
from rest_framework.generics import *


class BusCompanies(ListCreateAPIView):
    def get_queryset(self):
        return BusCompany.objects.all()

    def get_serializer_class(self):
        return BusCompanySerializer


class BusCompanyDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return BusCompany.objects.all()

    def get_serializer_class(self):
        return BusCompanySerializer


class Passenger(CreateAPIView):
    def get_queryset(self):
        return get_list_or_404(Passenger)

    def get_serializer_class(self):
        return PassengerSerializer

    def delete(self, request, pk):
        bus_company = get_object_or_404(BusCompany, pk=pk)
        bus_company.delete()

        return Response("Bus was deleted successfully", status.HTTP_204_NO_CONTENT)


class BusViewSet(ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bus_short_name', 'bus_company']
    search_fields = ['bus_short_name', ]
    ordering_fields = ['bus_short_name', 'bus_company']
    pagination_class = PageNumberPagination

    def delete(self, request, pk):
        bus = get_object_or_404(Bus, pk=pk)
        bus.delete()

        return Response("Bus was deleted successfully", status.HTTP_204_NO_CONTENT)


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def delete(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        route.delete()
        return Response("I tem was deleted", status.HTTP_204_NO_CONTENT)


class Tickets(ListCreateAPIView):
    def get_queryset(self):
        return Ticket.objects.all()

    def get_serializer_class(self):
        return TicketSerializer


class CalculateTicketPrice(RetrieveAPIView):
    def get_queryset(self):
        Route.objects.filter(bus=self.request.query_params['bus_short_name'])


class BusRoutes(ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bus']


class DepartureTimes(ModelViewSet):
    serializer_class = Route
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bus', 'starting_place', 'destination']
    search_fields = ['time', ]
    ordering_fields = ['bus_short_name', 'bus_company']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        routes = Route.objects.filter(bus=self.request.query_params.get('bus_short_name', None))
        times = []
        for route in routes:
            times.append(route.time.strftime("%H:%M"))
        return routes


class FindDepartureTimes(APIView):
    def get(self):
        times = []
        bus = Bus.objects.get(bus_short_name=self.request.query_params['bus_short_name'])
        routes = get_list_or_404(Route, bus=bus)
        for route in routes:
            times.append(route.time.strftime("%H:%M"))
        return Response(times)


class TicketsSold(ListAPIView):
    """This designates the list of tickets sold for a specified bus, at a specified
    departure date and time"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bus', 'departure_date']


class NumberOfSeatsTaken(APIView):
    def get(self):
        bus = dbus.service.Object.getT(pk=self.request.query_params.get('bus_short_name', None))
        tickets = Ticket.objects.filter(bus=bus, departure_date=self.request.query_params.get('departure_date', None),
                                        departure_time=self.request.query_params.get('departure-time', None))
        total_number = tickets.count()
        return Response(total_number)


class SeatsTaken(APIView):
    def get(self):
        tickets = Ticket.objects.filter(bus=self.request.query_params['bus_short_name'],
                                        departure_date=self.request.query_params['departure_date'],
                                        departure_time=self.request.query_params['departure_time'])
        seats_taken = [ticket.seat_number for ticket in tickets]
        return Response(seats_taken)


@api_view()
def is_fully_booked(request, bus_short_name: Bus, departure_date, departure_time):
    """
    Designates whether the specified bus is fully booked for the specified date and time.
    """
    if number_of_seats_taken(bus_short_name=bus_short_name, departure_date=departure_date,
                             departure_time=departure_time) == bus_short_name.number_of_seats:
        return Response('fully booked')
    else:
        return Response('not fully booked')


@api_view()
def is_seat_available(request, seat_number, bus_short_name, departure_date, departure_time):
    """Designates whether the specified seat number has already been taken for
    the specified date and time"""
    seats = []
    tickets = Ticket.objects.filter(bus=bus_short_name, departure_date=date.fromisoformat(departure_date),
                                    departure_time=time.fromisoformat(departure_time))
    for ticket in tickets:
        seats.append(ticket.seat_number)
    if seat_number not in seats:
        return Response('available')
    else:
        return Response('taken')


class SeatsAvailable(APIView):
    def get(self, *args, **kwargs):
        bus = Bus.objects.get(bus_short_name=self.request.query_params.get('bus_short_name', 'None'))
        tickets = Ticket.objects.filter(bus=bus, departure_date=self.request.query_params.get('departure_date', None),
                                        departure_time=self.request.query_params.get('departure_time', None))
        seats = [ticket.seat_number for ticket in tickets]
        list_of_seats_available = [number for number in range(1, bus.number_of_seats) if number not in seats]
        return Response(list_of_seats_available)


class TicketDetail(APIView):
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketSerializer(data=request.data, instance=ticket)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def delete(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.delete()
        return Response("I tem was deleted", status.HTTP_204_NO_CONTENT)


@api_view()
def number_of_seats_taken(request, bus_short_name, departure_date, departure_time):
    """The total number of tickets sold for a specified bus at a specified time"""
    bus = get_object_or_404(Bus, pk=bus_short_name)
    tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(departure_date),
                                    departure_time=time.fromisoformat(departure_time))
    total_number_sold = tickets.count()
    return Response(total_number_sold)


@api_view()
def seats_taken(request, bus_short_name, departure_date, departure_time):
    """Getting the list of seats that are already taken for a specified date and time"""
    seats = []
    tickets = Ticket.objects.filter(bus=bus_short_name, departure_date=date.fromisoformat(departure_date),
                                    departure_time=time.fromisoformat(departure_time))
    for ticket in tickets:
        seats.append(ticket.seat_number)
    return Response(seats)


@api_view()
def is_fully_booked(request, bus_short_name: Bus, departure_date, departure_time):
    """
    Designates whether the specified bus is fully booked for the specified date and time.
    """
    if number_of_seats_taken(bus_short_name=bus_short_name, departure_date=departure_date,
                             departure_time=departure_time) == bus_short_name.number_of_seats:
        return Response('fully booked')
    else:
        return Response('not fully booked')


@api_view()
def is_seat_available(request, seat_number, bus_short_name, departure_date, departure_time):
    """Designates whether the specified seat number has already been taken for
    the specified date and time"""
    seats = []
    tickets = Ticket.objects.filter(bus=bus_short_name, departure_date=date.fromisoformat(departure_date),
                                    departure_time=time.fromisoformat(departure_time))
    for ticket in tickets:
        seats.append(ticket.seat_number)
    if seat_number not in seats:
        return Response('available')
    else:
        return Response('taken')


@api_view()
def seats_available(request, bus_short_name, departure_date, departure_time):
    seats = []
    bus = get_object_or_404(Bus, bus_short_name=bus_short_name)  # Important for review later.
    tickets = Ticket.objects.filter(bus=bus_short_name, departure_date=date.fromisoformat(departure_date),
                                    departure_time=time.fromisoformat(departure_time))
    for ticket in tickets:
        seats.append(ticket.seat_number)

    list_of_seats_available = []
    for number in range(1, bus.number_of_seats):
        if number not in seats:
            list_of_seats_available.append(number)
        return Response(list_of_seats_available)
