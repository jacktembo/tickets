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
        route_id = request.POST.get('route', False)
        route = Route.objects.get(id=int(route_id))
        bus = route.bus
        total_number_of_seats = bus.number_of_seats
        route_time = route.time

        def seat_status(seat_number):
            if seat_number in seats_taken:
                return 'taken'
            elif seat_number in seats_not_taken:
                return 'available'
            else:
                return 'this is not a valid seat'

        # return HttpResponse({seat: seat_status(seat) for seat in all_seats})
        tickets = Ticket.objects.filter(route__bus=bus, departure_date=departure_date, route__time=route_time)
        seats_taken = [ticket.seat_number for ticket in tickets]
        seats_not_taken = [seat for seat in range(1, total_number_of_seats + 1) if seat not in seats_taken]
        all_seats = sorted(seats_taken + seats_not_taken)
        seats = {seat: seat_status(seat) for seat in all_seats}
        bus_company = request.POST.get('bus-company', False)
        context = {
            'bus_company': bus_company, 'route': route, 'client_full_name': client_full_name,
            'client_phone_number': client_phone_number, 'departure_date': departure_date,
            'seats': seats,
        }
        return render(request, 'select_seat_number.html', context)


def select_seat(request):
    route_id = request.POST.get('route', False)
    route = Route.objects.get(id=int(route_id))
    bus = route.bus
    total_number_of_seats = bus.number_of_seats
    route_time = route.time

    def seat_status(seat_number):
        if seat_number in seats_taken:
            return 'taken'
        elif seat_number in seats_not_taken:
            return 'available'
        else:
            return 'this is not a valid seat'

    # return HttpResponse({seat: seat_status(seat) for seat in all_seats})
    client_full_name = request.POST.get('client-full-name', False)
    client_phone_number = request.POST.get('client-phone-number', False)
    departure_date = date.fromisoformat(request.POST.get('departure-date', False))
    tickets = Ticket.objects.filter(route__bus=bus, departure_date=departure_date, route__time=route_time)
    seats_taken = [ticket.seat_number for ticket in tickets]
    seats_not_taken = [seat for seat in range(1, total_number_of_seats + 1) if seat not in seats_taken]
    all_seats = sorted(seats_taken + seats_not_taken)
    seats = {seat: seat_status(seat) for seat in all_seats}
    bus_company = request.POST.get('bus-company', False)
    route = request.POST.get('route', False)
    my_list = [2, 5, 6]
    context = {
        'bus_company': bus_company, 'route': route, 'client_full_name': client_full_name,
        'client_phone_number': client_phone_number, 'departure_date': departure_date,
        'seats': seats, 'all_seats': all_seats, 'my_list': my_list
    }
    return render(request, 'select_seat_number.html', context)