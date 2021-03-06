from decimal import Decimal
from rest_framework import serializers
from .models import *


class BusCompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusCompanyImage
        fields = ['id', 'image', ]


class BusCompanySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('company_image')

    def company_image(self, bus_company: BusCompany):
        return bus_company.images.image.url

    class Meta:
        model = BusCompany
        fields = [
            'id', 'company_name', 'company_phone_number', 'company_email', 'address',
            'image',
        ]


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


class BulkRouteCreate(serializers.ListSerializer):
    def create(self, validated_data):
        route_data = [Route(**item) for item in validated_data]
        return Route.objects.bulk_create(route_data)


class RouteSerializer(serializers.ModelSerializer):
    bus = serializers.StringRelatedField()
    bus_company = serializers.SerializerMethodField('the_bus_company')
    list_serializer_class = BulkRouteCreate

    class Meta:
        model = Route
        fields = [
            'id', 'bus', 'bus_company', 'starting_place', 'destination', 'time', 'price', 'route_full_name',
            'route_slug_name',
        ]

    route_full_name = serializers.SerializerMethodField(method_name='full_route_name')
    route_slug_name = serializers.SerializerMethodField(method_name='slug_name')

    def full_route_name(self, route: Route):
        return route.__str__()

    def slug_name(self, route: Route):
        return f"{route.starting_place.title()}-{route.destination.title()}-{route.time.strftime('%H:%M')}-K{route.price}"

    def the_bus_company(self, route: Route):
        return route.bus.bus_company.company_name


class SeatSerializer(serializers.ModelSerializer):
    model = Seat
    fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('route_time')
    price = serializers.SerializerMethodField('ticket_price')
    route_slug_name = serializers.SerializerMethodField('the_route')
    target_bus_company = serializers.SerializerMethodField('bus_company')
    bus_name = serializers.SerializerMethodField('the_bus_name')

    def route_time(self, ticket: Ticket):
        return ticket.route.time.strftime('%H:%M')

    def ticket_price(self, ticket: Ticket):
        return ticket.route.price

    def the_route(self, ticket: Ticket):
        return ticket.route.__str__()

    def bus_company(self, ticket: Ticket):
        return ticket.route.bus.bus_company.company_name

    def the_bus_name(self, ticket: Ticket):
        return ticket.route.bus.bus_full_name

    class Meta:
        model = Ticket
        fields = [
            'ticket_number', 'bus_name', 'target_bus_company', 'passenger_phone', 'passenger_first_name',
            'passenger_last_name',
            'departure_date', 'seat_number', 'route', 'route_slug_name', 'time', 'price',
        ]


class BulkRouteCreate(serializers.ListSerializer):
    def create(self, validated_data):
        route_data = [Route(**item) for item in validated_data]
        return Route.objects.bulk_create(route_data)
