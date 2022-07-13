# from unittest import registerResult
# from django.http import HttpResponse
# from django.shortcuts import render
# from django_filters.rest_framework import DjangoFilterBackend
# from mysqlx import RowResult
# from rest_framework import status
# from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
# from rest_framework.decorators import api_view, APIView, permission_classes
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.generics import *
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from .serializers import *
# from core import kazang
# from core import phone_numbers
#
#
# class BusCompanies(ListCreateAPIView):
#     def get_queryset(self):
#         return BusCompany.objects.prefetch_related('images').all()
#
#     def get_serializer_class(self):
#         return BusCompanySerializer
#
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#
# class BusCompanyDetail(RetrieveUpdateDestroyAPIView):
#     def get_queryset(self):
#         return BusCompany.objects.all()
#
#     def get_serializer_class(self):
#         return BusCompanySerializer
#
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#
# class Passenger(CreateAPIView):
#     def get_queryset(self):
#         return get_list_or_404(Passenger)
#
#     def get_serializer_class(self):
#         return PassengerSerializer
#
#     def delete(self, request, pk):
#         bus_company = get_object_or_404(BusCompany, pk=pk)
#         bus_company.delete()
#
#         return Response("Bus was deleted successfully", status.HTTP_204_NO_CONTENT)
#
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#
# class BusViewSet(ModelViewSet):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['bus_short_name', 'bus_company']
#     search_fields = ['bus_short_name', ]
#     ordering_fields = ['bus_short_name', 'bus_company']
#
#     def delete(self, request, pk):
#         bus = get_object_or_404(Bus, pk=pk)
#         bus.delete()
#
#         return Response("Bus was deleted successfully", status.HTTP_204_NO_CONTENT)
#
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#
# class RouteViewSet(ModelViewSet):
#     permission_classes([IsAdminUser])
#
#     def get_queryset(self):
#         if 'bus-company' in self.request.query_params:
#             bus_company = self.request.query_params.get('bus-company', False)
#             if bus_company is not None:
#                 return Route.objects.filter(bus__bus_company_id=bus_company)
#         else:
#             return Route.objects.all()
#
#     serializer_class = RouteSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['bus', 'starting_place', 'destination', 'time', 'price']
#     search_fields = ['starting_place', 'destination', 'time']
#     ordering_fields = ['starting_place', 'destination', 'bus_company']
#
#     def delete(self, request, pk):
#         route = get_object_or_404(Route, pk=pk)
#         route.delete()
#         return Response("I tem was deleted", status.HTTP_204_NO_CONTENT)
#
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#
# class Tickets(ListCreateAPIView):
#     def get_queryset(self):
#         return Ticket.objects.filter(sold_offline=False)
#
#     def get_serializer_class(self):
#         return TicketSerializer
#
#     def post(self, request, *args, **kwargs):
#         amount = 22000
#         phone_number = self.request.data['passenger_phone']
#         if phone_numbers.get_network('passenger_phone') == 'airtel':
#             airtel_reference = self.request.data['airtel_reference']
#             query = kazang.airtel_pay_query(phone_number, amount, airtel_reference)
#             if query['response_code'] == 0:
#                 return self.create(request, *args, **kwargs)
#             else:
#                 return Response("Payment Declined")
#
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#
# class CalculateTicketPrice(RetrieveAPIView):
#     def get_queryset(self):
#         Route.objects.filter(bus=self.request.query_params['bus_short_name'])
#
#
# class DepartureTimes(ModelViewSet):
#     serializer_class = Route
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['bus', 'starting_place', 'destination']
#     search_fields = ['time', ]
#     ordering_fields = ['bus_short_name', 'bus_company']
#
#     def get_queryset(self):
#         routes = Route.objects.filter(bus=self.request.query_params.get('bus_short_name', None))
#         times = []
#         for route in routes:
#             times.append(route.time.strftime("%H:%M"))
#         return routes
#
#
# class FindDepartureTimes(APIView):
#     def get(self):
#         times = []
#         bus = Bus.objects.get(bus_short_name=self.request.query_params['bus_short_name'])
#         routes = get_list_or_404(Route, bus=bus)
#         for route in routes:
#             times.append(route.time.strftime("%H:%M"))
#         return Response(times)
#
#
# class TicketsSold(ListAPIView):
#     """This designates the list of tickets sold for a specified bus, at a specified
#     departure date and time"""
#     permission_classes = [IsAdminUser]
#     queryset = Ticket.objects.filter(sold_offline=False)
#     serializer_class = TicketSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = [
#         'bus', 'departure_date', 'date_bought', 'passenger_phone', 'passenger_first_name',
#         'passenger_last_name', 'seat_number', 'route', 'price', 'ticket_number',
#     ]
#
#
# class NumberOfSeatsTaken(APIView):
#     def get(self):
#         route = self.request.query_params.get('bus', None)
#         bus = route.bus
#         tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(
#             self.request.query_params.get('departure-date', None)))
#         total_number = tickets.count()
#         return Response(total_number)
#
#
# class Seats(APIView):
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#     def get(self, bus):
#         route_id = self.request.query_params['route-id']
#         route = Route.objects.get(id=route_id)
#         bus = route.bus
#         total_number_of_seats = bus.number_of_seats
#         departure_date = date.fromisoformat(self.request.query_params['departure-date'])
#         route_time = route.time
#         tickets = Ticket.objects.filter(route__bus=bus, departure_date=departure_date, route__time=route_time)
#         seats_taken = [ticket.seat_number for ticket in tickets]
#         seats_not_taken = [seat for seat in range(1, total_number_of_seats + 1) if seat not in seats_taken]
#         all_seats = sorted(seats_taken + seats_not_taken)
#
#         def seat_status(seat_number):
#             if seat_number in seats_taken:
#                 return 'taken'
#             elif seat_number in seats_not_taken:
#                 return 'available'
#             else:
#                 return 'this is not a valid seat'
#
#         return Response({seat: seat_status(seat) for seat in all_seats})
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def seats_available(request, route_id, departure_date):
#     route = Route.objects.get(id=route_id)
#     bus = route.bus
#     total_number_of_seats = bus.number_of_seats
#     tickets = Ticket.objects.filter(bus=bus, departure_date=departure_date)
#     seats_taken = [ticket.seat_number for ticket in tickets]
#     seats_not_taken = [seat for seat in range(1, total_number_of_seats + 1) if seat not in seats_taken]
#
#     return Response(seats_not_taken)
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def is_fully_booked(request, route_id, departure_date):
#     """
#     Designates whether the specified bus is fully booked for the specified date and time.
#     """
#     route = Route.objects.get(id=route_id)
#     bus = route.bus
#     if number_of_seats_taken(request, route_id=route_id, departure_date=departure_date,
#                              ) == bus.number_of_seats:
#         return Response('fully booked')
#     else:
#         return Response('not fully booked')
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def is_seat_available(request, route_id, departure_date, seat_number):
#     """Designates whether the specified seat number has already been taken for
#     the specified date and time"""
#     seats = []
#     route = Route.objects.get(id=route_id)
#     tickets = Ticket.objects.filter(bus=route.bus, departure_date=date.fromisoformat(departure_date),
#                                     )
#     for ticket in tickets:
#         seats.append(ticket.seat_number)
#     if seat_number not in seats:
#         return Response('available')
#     else:
#         return Response('taken')
#
#
# class SeatsAvailable(APIView):
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#     def get(self, *args, **kwargs):
#         bus = Bus.objects.get(bus_short_name=self.request.query_params.get('bus_short_name', 'None'))
#         tickets = Ticket.objects.filter(bus=bus, departure_date=self.request.query_params.get('departure_date', None),
#                                         departure_time=self.request.query_params.get('departure_time', None))
#         seats = [ticket.seat_number for ticket in tickets]
#         list_of_seats_available = [number for number in range(1, bus.number_of_seats) if number not in seats]
#         return Response(list_of_seats_available)
#
#
# class TicketDetail(APIView):
#     authentication_classes = [
#         TokenAuthentication, JWTAuthentication, BasicAuthentication,
#         SessionAuthentication,
#     ]
#     permission_classes = [
#         IsAdminUser
#     ]
#
#     def get(self, request, pk):
#         ticket = get_object_or_404(Ticket, pk=pk)
#         serializer = TicketSerializer(ticket)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         ticket = get_object_or_404(Ticket, pk=pk)
#         serializer = TicketSerializer(data=request.data, instance=ticket)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#     def delete(self, request, pk):
#         ticket = get_object_or_404(Ticket, pk=pk)
#         ticket = get_object_or_404(Ticket, pk=pk)
#         ticket.delete()
#         return Response("I tem was deleted", status.HTTP_204_NO_CONTENT)
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def number_of_seats_taken(request, route_id, departure_date):
#     """The total number of tickets sold for a specified bus at a specified time"""
#     route = Route.objects.get(id=route_id)
#     bus = get_object_or_404(Bus, pk=route.bus.bus_short_name)
#     tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(departure_date),
#                                     )
#     total_number_sold = tickets.count()
#     return Response(total_number_sold)
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def seats_taken(request, route_id, departure_date):
#     """Getting the list of seats that are already taken for a specified date and time"""
#     seats = []
#     route = Route.objects.get(id=route_id)
#     bus = route.bus
#     tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(departure_date))
#     for ticket in tickets:
#         seats.append(ticket.seat_number)
#     return Response(seats)
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def is_fully_booked(request, route_id, departure_date):
#     """
#     Designates whether the specified bus is fully booked for the specified date and time.
#
#     """
#     route = Route.objects.get(id=route_id)
#     bus = route.bus
#     tickets = Ticket.objects.filter(bus=bus, departure_date=date.fromisoformat(departure_date),
#                                     )
#     total_number_sold = tickets.count()
#
#     if total_number_sold == bus.number_of_seats:
#         return Response('fully booked')
#     else:
#         return Response('not fully booked')
#
#
# @api_view()
# @permission_classes([IsAdminUser])
# def is_seat_available(request, seat_number, route_id, departure_date):
#     """Designates whether the specified seat number has already been taken for
#     the specified date and time"""
#     route = Route.objects.get(id=route_id)
#     seats = []
#     tickets = Ticket.objects.filter(bus=route.bus, departure_date=date.fromisoformat(departure_date),
#                                     )
#     for ticket in tickets:
#         seats.append(ticket.seat_number)
#     if seat_number not in seats:
#         return Response('available')
#     else:
#         return Response('taken')
#
#
# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def sale_offline(request, route_id, departure_date, seat_number):
#     """
#     This is for making a ticket as sold in the station.
#     You have to send a POST request with an empty JSON object to the endpoint to
#     create an offline ticket.
#     """
#     if request.method == 'POST':
#         route = Route.objects.get(id=route_id)
#         bus = route.bus
#         ticket = Ticket.objects.create(
#             sold_offline=True, passenger_phone='N/A', passenger_first_name='N/A',
#             passenger_last_name='N/A', departure_date=departure_date, route=route,
#             seat_number=seat_number, scanned=True
#         )
#         return Response('sold offline ticket successfully', status=status.HTTP_201_CREATED)
#
#
# class ScanView(APIView):
#     """Logic for scanning a ticket."""
#     permission_classes = [IsAdminUser]
#     authentication_classes = [TokenAuthentication, SessionAuthentication, JWTAuthentication, BasicAuthentication]
#
#     def get(self, request, ticket_number, *args, **kwargs):
#         ticket = Ticket.objects.filter(ticket_number=ticket_number)
#         if ticket.exists() and not ticket.first().scanned:
#             ticket.update(scanned=True)
#             return Response('Verified Successfully')
#         elif ticket.exists() and ticket.first().scanned:
#             return Response('Ticket Already Scanned')
#         else:
#             return Response('Invalid Ticket')
#
#
# def index(request):
#     context = {
#
#     }
#     return render(request, 'index.html', context)
