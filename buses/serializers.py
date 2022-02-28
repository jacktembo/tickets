from decimal import Decimal
from rest_framework import serializers
from .models import *


class BusCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusCompany
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = [
            'id', 'first_name', 'last_name', 'phone',
        ]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        exclude = ('bus',)

    route_full_name = serializers.SerializerMethodField(method_name='full_route_name')
    route_slug_name = serializers.SerializerMethodField(method_name='slug_name')

    def full_route_name(self, route: Route):
        return route.__str__()

    def slug_name(self, route: Route):
        return f"{route.starting_place.title()}-{route.destination.title()}-{route.time.strftime('%H:%M')}-K{route.price}"


class SeatSerializer(serializers.ModelSerializer):
    model = Seat
    fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('route_time')
    price = serializers.SerializerMethodField('ticket_price')
    route_name = serializers.SerializerMethodField('the_route')

    def route_time(self, ticket: Ticket):
        return ticket.route.time.strftime('%H:%M')

    def ticket_price(self, ticket: Ticket):
        return ticket.route.price

    def the_route(self, ticket: Ticket):
        return ticket.route.__str__()


    class Meta:
        model = Ticket
        fields = [
            'ticket_number', 'bus', 'passenger_phone', 'passenger_first_name', 'passenger_last_name',
            'departure_date', 'seat_number', 'route', 'route_name', 'time', 'price',
        ]
