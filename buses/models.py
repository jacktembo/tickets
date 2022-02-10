from django.db import models


class BusCompany(models.Model):
    company_name = models.CharField(max_length=50)
    company_phone_number = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=64)
    address = models.CharField(max_length=100)
    number_of_buses = models.IntegerField(default=1)
    company_logo = models.ImageField()

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Bus Companies'


class Passenger(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Route(models.Model):
    """A route class e.g from Lusaka to Livingstone"""
    starting_place = models.CharField(max_length=50)
    to = models.CharField(max_length=50)
    full_route_name = models.CharField(max_length=100)
    time = models.TimeField()
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.full_route_name


class Bus(models.Model):
    """A bus representation"""
    name = models.CharField(max_length=50)
    number_of_seats = models.IntegerField()
    image = models.ImageField()
    routes = models.ManyToManyField(Route, related_name='buses')


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_available = models.BooleanField()
    verbose_name = models.CharField(max_length=50, blank=True, null=True)


class Ticket(models.Model):
    ticket_number = models.CharField(max_length=20)
    paid = models.BooleanField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    date_bought = models.DateField()
    passenger_first_name = models.CharField(max_length=50)
    passenger_last_name = models.CharField(max_length=50)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    def __str__(self):
        return self.ticket_number


