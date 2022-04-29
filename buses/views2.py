from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *


def index(request):
    bus_companies = BusCompany.objects.all()
    context = {
        'bus_companies': bus_companies
    }
    return render(request, 'index.html', context)