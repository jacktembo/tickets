from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core import phone_numbers, kazang
from core.kazang import session_uuid
from . import sms
from .models import *
from internal.models import *
all1zed_commission = int(All1zedBusCommission.objects.all()[0].commission_per_ticket)


def index(request):
    bus_companies = BusCompany.objects.all()
    context = {
        'bus_companies': bus_companies
    }
    return render(request, 'index.html', context)


def bus_company_detail(request, pk):
    bus_company = BusCompany.objects.get(pk=pk)
    routes = Route.objects.filter(bus__bus_company=bus_company).order_by('starting_place', 'destination')
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
                cash_in = kazang.mobile_cash_in(bus_mobile_money_number, deposit)
                try:
                    if cash_in.get('response_code', False) == '0':
                        Transaction.objects.create(
                            name='Bus Operator Cash In', type='cash_in', session_uuid=session_uuid,
                            status='successful', product_id=5305, amount=float(deposit),
                            phone_number=int(bus_mobile_money_number),
                            request_reference=cash_in.get('request_reference', None), provider_reference='N/A',
                        )
                    else:
                        Transaction.objects.create(
                            name='Bus Operator Cash In', type='cash_in', session_uuid=session_uuid,
                            status='failed', product_id=5305, amount=float(deposit),
                            phone_number=int(bus_mobile_money_number),
                            request_reference=cash_in.get('request_reference', None), provider_reference='N/A',
                        )
                except:
                    print('something went wrong')
                ticket.save()
                message = f"Dear {client_first_name} {client_last_name}, Your {bus.bus_company.company_name} Bus Ticket Number is {ticket.ticket_number}. Download your ticket at https://buses.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
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
            cash_in = kazang.mobile_cash_in(bus_mobile_money_number, deposit)
            try:
                if cash_in.get('response_code', False) == '0':
                    Transaction.objects.create(
                        name='Bus Operator Cash In', type='cash_in', session_uuid=session_uuid,
                        status='successful', product_id=5305, amount=float(deposit),
                        phone_number=int(bus_mobile_money_number),
                        request_reference=cash_in.get('request_reference', None), provider_reference='N/A',
                    )
                else:
                    Transaction.objects.create(
                        name='Bus Operator Cash In', type='cash_in', session_uuid=session_uuid,
                        status='failed', product_id=5305, amount=float(deposit),
                        phone_number=int(bus_mobile_money_number),
                        request_reference=cash_in.get('request_reference', None), provider_reference='N/A',
                    )
            except:
                print('something went wrong')
            ticket.save()
            message = f"Dear {client_first_name} {client_last_name}, Your {bus.bus_company.company_name} Bus Ticket Number is {ticket.ticket_number}. Download your ticket at https://buses.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets. "
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
                cash_in = kazang.mobile_cash_in(bus_mobile_money_number, deposit)
                try:
                    if cash_in.get('response_code', False) == '0':
                        Transaction.objects.create(
                            name='Bus Operator Cash In', type='cash_in', session_uuid=session_uuid,
                            status='successful', product_id=5305, amount=float(deposit),
                            phone_number=int(bus_mobile_money_number),
                            request_reference=cash_in.get('request_reference', None), provider_reference='N/A',
                        )
                    else:
                        Transaction.objects.create(
                            name='Bus Operator Cash In', type='cash_in', session_uuid=session_uuid,
                            status='failed', product_id=5305, amount=float(deposit),
                            phone_number=int(bus_mobile_money_number),
                            request_reference=cash_in.get('request_reference', None), provider_reference='N/A',
                        )
                except:
                    pass
                ticket.save()
                message = f"Dear {client_first_name} {client_last_name}, Your {bus.bus_company.company_name} Bus Ticket Number is {ticket.ticket_number}. Download your ticket at https://buses.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
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


def ticket(request):
    return render(request, 'ticket.html')


class DownloadView(WeasyTemplateResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        self.ticket_number = self.kwargs['ticket_number']
        ticket_number = self.ticket_number
        ticket = get_object_or_404(Ticket, ticket_number=ticket_number)
        bus = ticket.bus
        client_first_name = ticket.passenger_first_name
        client_last_name = ticket.passenger_last_name
        client_phone_number = ticket.passenger_phone
        departure_date = ticket.departure_date
        route = ticket.route
        departure_time = route.time.strftime("%H:%M hrs")
        seat_number = ticket.seat_number
        ticket_price = route.price
        bus_company_image_url = bus.bus_company.images.image.url
        qrcode_image_url = f'https://api.qrserver.com/v1/create-qr-code/?data={ticket_number}&size=200x200&format=svg'
        context = {
            'ticket': ticket, 'bus': bus, 'client_first_name': client_first_name,
            'client_last_name': client_last_name, 'client_phone_number': client_phone_number,
            'departure_date': departure_date, 'route': route, 'seat_number': seat_number,
            'ticket_price': ticket_price, 'qrcode_image_url': qrcode_image_url,
            'departure_time': departure_time, 'banner_image_url': bus_company_image_url,
            'ticket_number': ticket_number
        }
        return context

    template_name = 'ticket.html'

    def get_pdf_filename(self):
        return f'All1Zed-ticket-{self.ticket_number}.pdf'


def scan_ticket(ticket_number):
    ticket = Ticket.objects.filter(ticket_number=ticket_number)
    if ticket.exists() and not ticket.first().scanned:
        ticket.update(scanned=True)
        return 'verified'
    elif ticket.exists() and ticket.first().scanned:
        return 'scanned'
    else:
        return 'invalid'


@api_view()
def scan_ticket_api(request, ticket_number):
    ticket = Ticket.objects.filter(ticket_number=ticket_number)
    if ticket.exists() and not ticket.first().scanned:
        ticket.update(scanned=True)
        return Response({'status': 'success', 'message': 'Verified Successfully',
                         'full_name': ticket.first().passenger_first_name + " " + ticket.first().passenger_last_name,
                         'phone_number': ticket.first().passenger_phone,
                         })
    elif ticket.exists() and ticket.first().scanned:
        return Response({'status': 'failed', 'message': 'Already Scanned',
                         'full_name': f"{ticket.first().passenger_first_name} {ticket.first().passenger_last_name}",
                         'phone_number': ticket.first().passenger_phone,
                         })
    else:
        return Response({'status': 'failed', 'message': 'Invalid Ticket Number'})


def scan_by_ticket_number(request):
    if request.method == 'GET':
        return render(request, 'verify_ticket.html')
    elif request.method == 'POST':
        ticket_number = request.POST.get('ticket_number', False)
        if scan_ticket(ticket_number) == 'verified':
            messages.success(request, 'Verified Successfully')
            return redirect('verify-by-ticket-number')
        elif scan_ticket(ticket_number) == 'scanned':
            messages.error(request, 'Ticket Already Scanned')
            return redirect('verify-by-ticket-number')
        elif scan_ticket(ticket_number) == ('invalid'):
            messages.error(request, 'Invalid Ticket Number!')
            return redirect('verify-by-ticket-number')
        else:
            return HttpResponse(str(scan_ticket(ticket_number)) == 'yoo')


def terms(request):
    terms = TermsAndConditions.objects.all().first()
    context = {
        'terms': terms
    }
    return render(request, 'terms_and_conditions.html', context)

def bus_operator(request):
    buses = Bus.objects.filter(bus_admin=request.user)
    context = {
        'buses': buses,
    }
    return render(request, 'bus_operator.html', context)


def manage_bus(request, pk):
    bus = Bus.objects.get(pk=pk)
    total_number_of_seats = bus.number_of_seats

    def seat_status(seat_number):
        if seat_number in seats_taken:
            return 'taken'
        elif seat_number in seats_not_taken:
            return 'available'
        else:
            return 'this is not a valid seat'


    departure_date = date.today()
    tickets = Ticket.objects.filter(route__bus=bus, departure_date=departure_date)
    seats_taken = [ticket.seat_number for ticket in tickets]
    seats_not_taken = [seat for seat in range(1, total_number_of_seats + 1) if seat not in seats_taken]
    all_seats = sorted(seats_taken + seats_not_taken)
    def person_on_seat(seat_number=1):
        ticket = Ticket.objects.filter(departure_date=departure_date, route__bus=bus, seat_number=int(seat_number))
        if ticket.exists():
            person = {
                'first_name': ticket.first().passenger_first_name, 'last_name': ticket.first().passenger_last_name,
                'phone_number': ticket.first().passenger_phone, 'ticket_number': ticket.first().ticket_number,
                'already_scanned': 'Yes' if ticket.first().scanned else 'No'
            }
            return person
        else:
            person = {
                'first_name': 'N/A', 'last_name': 'N/A', 'phone_number': 'N/A',
            }
            return person

    seats = {'first': {seat: seat_status(seat) for seat in all_seats}, 'second': {seat: person_on_seat(seat) for seat in all_seats}}

    context = {
        'bus': bus, 'departure_date': departure_date, 'seats_taken': seats_taken,
        'seats_not_taken': seats_not_taken, 'all_seats': all_seats,
        'seats': seats, 'person': person_on_seat(),
    }
    return render(request, 'seat_operation.html', context)


def sale_offline(request, pk, seat_number):
    bus = Bus.objects.get(pk=pk)
    seat_number = int(seat_number)
    routes = Route.objects.filter(bus=bus)
    if request.method == 'GET':

        context = {
            'pk': pk, 'seat_number': seat_number, 'routes': routes,
            'bus': bus,
        }
        return render(request, 'sale_offline.html', context)

    elif request.method == 'POST':
        seat_number = int(request.POST.get('seat-number', False))
        departure_date = date.today()
        route = Route.objects.get(id=int(request.POST.get('route', False)))

        Ticket.objects.create(
            sold_offline=True, scanned=True, passenger_phone='N/A', passenger_first_name='N/A',
            passenger_last_name='N/A', departure_date=departure_date, route=route,
            seat_number=seat_number
        )
        return HttpResponseRedirect(reverse('manage-bus', kwargs={'pk': pk}))
