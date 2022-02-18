from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import *
from .serializers import *
from rest_framework.generics import *


class Passenger(APIView):
    def post(self, request):
        serializer = PassengerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class Buses(APIView):
    def get(self, request):
        bus = get_list_or_404(Bus)
        serializer = BusSerializer(bus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class BusDetail(APIView):
    def get(self, request, pk):
        bus = get_object_or_404(Bus, pk=pk)
        serializer = BusSerializer(bus)
        return Response(serializer.data)

    def put(self, request, pk):
        bus = get_object_or_404(Bus, pk=pk)
        serializer = BusSerializer(data=request.data, instance=bus)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, )

    def delete(self, request, pk):
        bus = get_object_or_404(Bus, pk=pk)
        bus.delete()
        return Response("I tem was deleted", status.HTTP_204_NO_CONTENT)


class Routes(APIView):
    def get(self, request):
        routes = get_list_or_404(Route)
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class RouteDetail(APIView):
    def get(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    def put(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        serializer = RouteSerializer(data=request.data, instance=route)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, )

    def delete(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        route.delete()
        return Response("I tem was deleted", status.HTTP_204_NO_CONTENT)


class Tickets(APIView):
    def get(self, request):
        ticket = get_list_or_404(Ticket)
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


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


class CalculateTicketPrice(APIView):
    def get(self, bus_short_name, route_id):
        bus = get_object_or_404(Bus, bus_short_name=bus_short_name)
        route = get_object_or_404(Route, id=route_id, bus=bus)

        return Response(route.price)


@api_view()
def find_bus_routes(request, bus_short_name):
    routes = get_list_or_404(Route, bus=bus_short_name)
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)


@api_view()
def find_departure_times(request, bus_short_name):
    times = []
    routes = get_list_or_404(Route, bus=bus_short_name)
    for route in routes:
        times.append(route.time.strftime("%H:%M"))
    return Response(times)


@api_view()
def tickets_sold(request, bus_short_name, departure_date, departure_time):
    """
    This designates the queryset for all the tickets sold for the specified bus on a
    specified date and time.
    """
    bus = get_object_or_404(Bus, pk=bus_short_name)
    tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(departure_date),
                                    departure_time=time.fromisoformat(departure_time))
    tickets = TicketSerializer(tickets, many=True)
    return Response(tickets.data)  # Returning a JSON list of sold tickets for a bus.


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
    seats_available = []
    for number in range(1, bus.number_of_seats):
        if number not in seats:
            seats_available.append(number)
        return Response(seats_available)
