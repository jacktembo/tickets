from django.contrib import admin
from .models import *

admin.site.register([Bus, Passenger, Ticket, Route, Seat])