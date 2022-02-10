import site
from django.contrib import admin
from .models  import *

admin.site.register(BusCompany)
admin.site.register(Route)