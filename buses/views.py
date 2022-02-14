from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import *
from .serializers import *


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


@api_view(['GET'])
def calculate_ticket_price(request, bus_short_name, route_id):
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