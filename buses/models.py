from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404, get_list_or_404
import secrets
import string
from datetime import date, datetime, timedelta, time


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
    bus_company = models.OneToOneField(BusCompany, on_delete=models.CASCADE, related_name='images')
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
    bus_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, related_name='buses')
    bus_full_name = models.CharField(max_length=50)
    bus_short_name = models.CharField(max_length=20, primary_key=True, editable=False)
    number_of_seats = models.IntegerField()
    mobile_money_number = models.CharField(max_length=10, help_text='Enter the 10 digit Mobile Money number for receiving money.')

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
        s = (self.bus_company.company_name[:4] + str(query + 1)).lower()
        self.bus_short_name = "".join(s.split())
        super(Bus, self).save(*args, **kwargs)

class Route(models.Model):
    """A route class e.g from Lusaka to Livingstone"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='route')
    starting_place = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    time = models.TimeField()
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f'{self.starting_place}-{self.destination}-{self.time.strftime("%H:%M")}-K{self.price}'



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


class Ticket(models.Model):
    """A ticket that has been successfully paid for and generated.

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    ticket_number = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    date_bought = models.DateField(auto_now_add=True)
    passenger_phone = models.CharField(max_length=12)
    passenger_first_name = models.CharField(max_length=50)
    passenger_last_name = models.CharField(max_length=50)
    departure_date = models.DateField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    sold_offline = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    scanned = models.BooleanField(default=False, help_text='Designates whether a Ticket has already been scanned')

    def __str__(self):
        return self.ticket_number

    def save(self, *args, **kwargs):
        # bus = Bus.objects.get(bus_short_name=self.route.bus.bus_short_name)
        alphabet = string.digits
        ticket_digits = ''.join(secrets.choice(alphabet) for i in range(8))
        self.ticket_number = self.route.bus.bus_short_name[:2].upper() + ticket_digits
        self.price = self.route.price
        self.bus = self.route.bus
        super(Ticket, self).save(*args, **kwargs)


