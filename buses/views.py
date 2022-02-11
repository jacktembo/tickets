from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal


@api_view(['GET', 'POST'])
def all_1_zed_ticket_API(request):
    return Response({'bus_name': 'Powertools', 'ticket_number': 225675455})
