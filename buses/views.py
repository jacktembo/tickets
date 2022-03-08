from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.routers import DefaultRouter
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .models import *
from .serializers import *
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime, date, timedelta, time


class BusCompanies(ListCreateAPIView):
    def get_queryset(self):
        return BusCompany.objects.prefetch_related('bus_company_image').all()

    def get_serializer_class(self):
        return BusCompanySerializer


class BusCompanyDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return BusCompany.objects.all()

    def get_serializer_class(self):
        return BusCompanySerializer

    permission_classes = [IsAuthenticated]


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

    def delete(self, request, pk):
        bus = get_object_or_404(Bus, pk=pk)
        bus.delete()

        return Response("Bus was deleted successfully", status.HTTP_204_NO_CONTENT)


class RouteViewSet(ModelViewSet):
    def get_queryset(self):
        if 'bus-company' in self.request.query_params:
            bus_company = self.request.query_params.get('bus-company', False)
            if bus_company is not None:
                return Route.objects.filter(bus__bus_company_id=bus_company)
        else:
            return Route.objects.all()

    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bus', 'starting_place', 'destination', 'time', 'price']
    search_fields = ['starting_place', 'destination', 'time']
    ordering_fields = ['starting_place', 'destination', 'bus_company']

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


class DepartureTimes(ModelViewSet):
    serializer_class = Route
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bus', 'starting_place', 'destination']
    search_fields = ['time', ]
    ordering_fields = ['bus_short_name', 'bus_company']

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
        bus = Bus.objects.get(pk=self.request.query_params.get('bus', None))
        tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(
            self.request.query_params.get('departure-date', None)),
                                        departure_time=self.request.query_params.get('departure-time', None))
        total_number = tickets.count()
        return Response(total_number)


class Seats(APIView):
    def get(self, bus):
        route_id = self.request.query_params['route-id']
        route = Route.objects.get(id=route_id)
        bus = route.bus
        total_number_of_seats = bus.number_of_seats
        departure_date = date.fromisoformat(self.request.query_params['departure-date'])
        route_time = route.time
        tickets = Ticket.objects.filter(route__bus=bus, departure_date=departure_date, route__time=route_time)
        seats_taken = [ticket.seat_number for ticket in tickets]
        seats_not_taken = [seat for seat in range(1, total_number_of_seats + 1) if seat not in seats_taken]
        all_seats = sorted(seats_taken + seats_not_taken)

        def seat_status(seat_number):
            if seat_number in seats_taken:
                return 'taken'
            elif seat_number in seats_not_taken:
                return 'available'
            else:
                return 'this is not a valid seat'

        return Response({seat: seat_status(seat) for seat in all_seats})


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
