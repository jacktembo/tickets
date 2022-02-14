from decimal import Decimal
from rest_framework import serializers
from .models import *


# class BusCompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusCompany
#         fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


# class BusCompanyImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusCompanyImage
#         fields = [
#             'id', 'bus_company', 'image',
#         ]


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = [
            'id', 'first_name', 'last_name', 'phone',
        ]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

    route_full_name = serializers.SerializerMethodField(method_name='full_route_name')

    def full_route_name(self, route: Route):
        return route.__str__()


class SeatSerializer(serializers.ModelSerializer):
    model = Seat
    fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
