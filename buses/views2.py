from datetime import datetime, date, time, timedelta

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
    if request.method == 'GET':

        context = {
            'bus_company': bus_company, 'routes': routes
        }
        return render(request, 'bus_detail.html', context)
    elif request.method == 'POST':
        context = {

        }
        client_full_name = request.POST.get('client-full-name', False)
        client_phone_number = request.POST.get('client-phone-number', False)
        departure_date = date.fromisoformat(request.POST.get('departure-date', False))
        route = request.POST.get('route', False)
        route = Route.objects.get(pk=int(route))
        context = {
            'bus_company': bus_company, 'route': route, 'client_full_name': client_full_name,
            'client_phone_number': client_phone_number, 'departure_date': departure_date,
        }
        return render(request, 'select_seat_number.html', context)


def select_seat(request):
    client_full_name = request.POST.get('client-full-name', False)
    client_phone_number = request.POST.get('client-phone-number', False)
    departure_date = date.fromisoformat(request.POST.get('departure-date', False))
    bus_company = request.POST.get('bus-company', False)
    route = request.POST.get('route', False)
    context = {
        'bus_company': bus_company, 'route': route, 'client_full_name': client_full_name,
        'client_phone_number': client_phone_number, 'departure_date': departure_date,
    }
    return render(request, 'select_seat_number.html', context)