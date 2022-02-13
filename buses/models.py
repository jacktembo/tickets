from django.db import models


# class BusCompany(models.Model):
#     """A company that owns bus(s)

#     Args:
#         models ([type]): [description]

#     Returns:
#         [type]: [description]
#     """
#     company_name = models.CharField(max_length=50)
#     company_phone_number = models.CharField(max_length=50)
#     company_email = models.EmailField(max_length=64)
#     address = models.CharField(max_length=100)

#     def __str__(self):
#         return self.company_name


# class BusCompanyImage(models.Model):
#     """An image or logo of a bus company. 

#     Args:
#         models ([type]): [description]
#     """
#     bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='tickets/buscompanies')


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


class Route(models.Model):
    """A route class e.g from Lusaka to Livingstone"""
    starting_place = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    time = models.TimeField()
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f'{self.starting_place} to {self.destination}'


class Bus(models.Model):
    """A bus representation"""
    name = models.CharField(max_length=50)
    number_of_seats = models.IntegerField()
    image = models.ImageField(blank=True, null=True)
    routes = models.ManyToManyField(Route, related_name='buses')

    def __str__(self):
        return self.name


class BusImage(models.Model):
    """The image(s) of a bus. A bus can have multliple images.

    Args:
        models ([type]): [description]
    """
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tickets/buses')


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
    """A ticket that has been sucessfully paid for and generated.

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    ticket_number = models.CharField(max_length=20, primary_key=True)
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
