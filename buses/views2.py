from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *


def index(request):
    bus_companies = BusCompany.objects.all()
    context = {
        'bus_companies': bus_companies
    }
    return render(request, 'index.html', context)


def bus_company_detail(request, pk):
    bus_company = BusCompany.objects.get(pk=pk)
    routes = Route.objects.filter(bus__bus_company=bus_company)
    context = {
        'bus_company': bus_company, 'routes': routes
    }
    return render(request, 'bus_detail.html', context)
