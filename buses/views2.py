from datetime import datetime, date, time, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from core import phone_numbers, kazang
from . import sms
from .models import *

all1zed_commission = 1


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
        client_first_name = request.POST.get('client-first-name', False)
        client_last_name = request.POST.get('client-last-name', False)
        client_phone_number = request.POST.get('client-phone-number', False)
        departure_date = request.POST.get('departure-date', False)
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
            'bus_company': bus_company, 'route': route, 'client_first_name': client_first_name,
            'client_last_name': client_last_name,
            'client_phone_number': client_phone_number, 'departure_date': departure_date,
            'seats': seats,
        }
        return render(request, 'select_seat_number.html', context)


def mobile_payment(request):
    if request.method == "POST":
        client_phone_number = request.POST.get('client-phone-number', False)
        client_first_name = request.POST.get('client-first-name', False)
        client_last_name = request.POST.get('client-last-name', False)
        departure_date = request.POST.get('departure-date', False)
        route = Route.objects.get(pk=int(request.POST.get('route', False)))
        seat_number = int(request.POST.get('seat-number', False))
        bus = route.bus
        ticket_price = route.price
        bus_mobile_money_number = bus.mobile_money_number
        charge = (float(ticket_price) * 100) + (0.02 * float(ticket_price) * 100)
        context = {
            'client_phone_number': client_phone_number, 'client_first_name': client_first_name,
            'client_last_name': client_last_name, 'departure_date': departure_date,
            'route': route, 'seat_number': seat_number,
            'bus_mobile_money_number': bus_mobile_money_number, 'amount': charge,
        }

        if phone_numbers.get_network(client_phone_number) == 'airtel':
            pay = kazang.airtel_pay_payment(client_phone_number, charge)
            context['reference_number'] = pay.get('airtel_reference', False)
            return render(request, 'payment_waiting.html', context)

        elif phone_numbers.get_network(client_phone_number) == 'mtn':
            pay = kazang.mtn_debit(client_phone_number, charge)
            context['reference_number'] = pay.get('supplier_transaction_id', False)
            return render(request, 'payment_waiting.html', context)

        elif phone_numbers.get_network(client_phone_number) == 'zamtel':
            ticket = Ticket(bus=bus, passenger_phone=client_phone_number, passenger_first_name=client_first_name,
                            passenger_last_name=client_last_name, departure_date=departure_date,
                            seat_number=seat_number, route=route,
                            )
            deposit = (float(ticket_price) * 100) - (float(all1zed_commission * 100))
            pay = kazang.zamtel_money_pay(client_phone_number, charge)
            if pay.get('response_code', False) == '0':
                kazang.mobile_cash_in(bus_mobile_money_number, deposit)
                ticket.save()
                message = f"Dear {client_first_name} {client_last_name}, Your {bus.bus_company.company_name} Ticket Number is {ticket.ticket_number}. Download your ticket at https://buses.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
                sms.send_sms(client_phone_number, message)
                context = {
                    'ticket_number': ticket.ticket_number, 'client_first_name': client_first_name,
                    'client_last_name': client_last_name,
                    'ticket_price': ticket_price, 'bus': bus, 'route': route,
                }
                return render(request, 'payment_success.html', context)
            else:
                return HttpResponse(pay['response_message'])
        else:
            return HttpResponse('invalid phone number')


def payment_approval(request):
    reference_number = request.POST.get('reference-number', False)
    route_id = request.POST.get('route', False)
    route = Route.objects.get(pk=int(route_id))
    bus = route.bus
    departure_date = date.fromisoformat(request.POST.get('departure-date', False))
    bus_mobile_money_number = route.bus.mobile_money_number
    ticket_price = route.price
    charge = (float(ticket_price) * 100) + (0.02 * float(ticket_price) * 100)
    client_first_name = request.POST.get('client-first-name', False)
    client_last_name = request.POST.get('client-last-name', False)
    client_phone_number = request.POST.get('client-phone-number')
    seat_number = request.POST.get('seat-number', False)
    ticket = Ticket(bus=bus, passenger_phone=client_phone_number, passenger_first_name=client_first_name,
                    passenger_last_name=client_last_name, departure_date=departure_date,
                    seat_number=seat_number, route=route,
                    )
    deposit = (float(ticket_price) * 100) - (float(all1zed_commission * 100))
    if phone_numbers.get_network(client_phone_number) == 'airtel':
        r = kazang.airtel_pay_query(client_phone_number, charge, reference_number)
        if r.get('response_code', False) == '0':
            kazang.mobile_cash_in(bus_mobile_money_number, deposit)
            ticket.save()
            message = f"Dear {client_first_name}, Your {bus.bus_company.company_name} Ticket Number is {ticket.ticket_number}. Download your ticket at https://buses.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets. "
            sms.send_sms(client_phone_number, message)
            context = {
                'ticket_number': ticket.ticket_number, 'client_first_name': client_first_name,
                'client_last_name': client_last_name,
                'ticket_price': ticket_price, 'route': route
            }
            return render(request, 'payment_success.html', context)
        else:
            return HttpResponse('Transaction Failed. Please Try Again')

    elif phone_numbers.get_network(client_phone_number) == 'mtn':
        reference_number = request.POST.get('reference-number', False)
        approval = kazang.mtn_debit_approval(client_phone_number, charge, reference_number)
        if approval['response_code'] == '0':
            confirmation_number = approval['confirmation_number']
            debit_approval_confirm = kazang.mtn_debit_approval_confirm(client_phone_number, charge, confirmation_number)
            if debit_approval_confirm['response_code'] == '0':
                kazang.mobile_cash_in(bus_mobile_money_number, deposit)
                ticket.save()
                message = f"Dear {client_first_name} {client_last_name}, Your {bus.bus_company.company_name} Ticket Number is {ticket.ticket_number}. Download your ticket at https://buses.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
                sms.send_sms(client_phone_number, message)
                context = {
                    'ticket_number': ticket.ticket_number, 'client_first_name': client_first_name,
                    'client_last_name': client_last_name,
                    'ticket_price': ticket_price, 'bus': bus, 'route': route,
                }
                return render(request, 'payment_success.html', context)
            else:
                return HttpResponse('There was a problem processing your transaction. Please try again.')
        else:
            return HttpResponse('There was a problem processing your transaction. Please try again.')

