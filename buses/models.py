from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
import secrets
import string
from datetime import date, datetime, timedelta, time

from rest_framework import status
from rest_framework.response import Response


class BusCompany(models.Model):
    """A company that owns bus(s)

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Login Username')  # Admin user account for the Bus Company.
    company_name = models.CharField(max_length=50)
    company_phone_number = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=64)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Bus Companies'

    def __str__(self):
        return self.company_name


class BusCompanyImage(models.Model):
    """An image or logo of a bus company.

    Args:
        models ([type]): [description]
    """
    bus_company = models.OneToOneField(BusCompany, on_delete=models.CASCADE, related_name='bus_company_image')
    image = models.ImageField(upload_to='tickets/buscompanies', verbose_name='Upload Company Logo')


class Passenger(models.Model):
    """A person who wants to or who has purchased a bus ticket

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Bus(models.Model):
    """A bus representation"""
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, related_name='buses')
    bus_full_name = models.CharField(max_length=50)
    bus_short_name = models.CharField(max_length=20, primary_key=True, editable=False)
    number_of_seats = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Buses'

    def make_fully_booked(self):
        pass

    def __str__(self):
        return self.bus_full_name

    def save(self, *args, **kwargs):
        """
        Overriding the save method to create calculated field values.
        """
        query = Bus.objects.filter(bus_company=self.bus_company).count()
        # Computing the bus unique identifier below
        self.bus_short_name = "".join((self.bus_company.company_name[:4] + str(query + 1)).lower().strip().split())
        super(Bus, self).save(*args, **kwargs)


class Route(models.Model):
    """A route class e.g from Lusaka to Livingstone"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='route')
    starting_place = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    time = models.TimeField()
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f'{self.starting_place.title()}-{self.destination.title()}-K{self.price}'


class BusImage(models.Model):
    """The image(s) of a bus. A bus can have multliple images.

    Args:
        models ([type]): [description]
    """
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='tickets/buses', verbose_name='Upload Bus Image')


class Seat(models.Model):
    """A seat on a bus. One seat for one passenger.

    Args:
        models ([type]): [description]
    """
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_available = models.BooleanField()
    verbose_name = models.CharField(max_length=50, blank=True, null=True)


def validate_seat_number(route, seat_number, departure_date):
    if Ticket.objects.filter(route=route, seat_number=seat_number, departure_date=departure_date).exists():
        return Response('Seat number already taken', status=status.HTTP_400_BAD_REQUEST)
    else:
        return True


class Ticket(models.Model):
    """A ticket that has been sucessfully paid for and generated.

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    ticket_number = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    date_bought = models.DateField(auto_now_add=True)
    passenger_phone = models.CharField(max_length=12)
    passenger_first_name = models.CharField(max_length=50)
    passenger_last_name = models.CharField(max_length=50)
    departure_date = models.DateField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    def __str__(self):
        return self.ticket_number

    def save(self, *args, **kwargs):
        # bus = Bus.objects.get(bus_short_name=self.route.bus.bus_short_name)
        alphabet = string.ascii_letters + string.digits
        bus_short_name = self.route.bus.bus_short_name
        while True:
            ticket_number = ''.join(secrets.choice(alphabet) for i in range(10))
            available_tickets = [ticket.ticket_number for ticket in Ticket.objects.all()]
            proposed_ticket_number = f'{bus_short_name}-{ticket_number}'
            if proposed_ticket_number not in available_tickets:
                self.ticket_number = proposed_ticket_number
                break
            else:
                continue
        assert validate_seat_number(self.route, self.seat_number, self.departure_date) == True

        super(Ticket, self).save(*args, **kwargs)


class FullyBookedBus(models.Model):
    """
    Represents a bus that has been marked as fully booked by the admin, for a specified
    date and time.
    """
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_date = models.DateField()
    departure_time = models.TimeField()

    def __str__(self):
        return self.bus


class OfflineSoldSeat(models.Model):
    """
    A seat that has been marked as sold at a station by the admin.
    """
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    departure_date = models.DateField()
    departure_time = models.TimeField()
