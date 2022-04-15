from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import openpyxl
from core.buses.models import Route, Bus


def index(request):
    return render(request, 'index.html')

class BulkRoutesUpload(View):
    template_name = 'bulk_routes_upload'

    def get(self, request):
        return render(request, 'bulk_routes_upload.html')

    def post(self, request):
        file = request.FILES['file']
        maximum_rows = request.POST.get('maximum-rows', False)
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        routes = []
        obj_list = []

        for value in sheet.iter_rows(
                min_row=3, max_row=int(maximum_rows), min_col=2, max_col=5,
                values_only=True):
            routes.append(value)
        bus = Bus.objects.get(pk=request.POST.get('bus', False))

        for item in routes:
            a, b, c, d = item
            #     # print(f'Route(starting_place={a}, destination={b}, departure_time={c}, price={d})')
            obj_list.append(Route(bus=bus, starting_place=a, destination=b, time=c, price=d))
        #     # print(Route(a, b, c, d))
        #     result = Route.objects.create(bus=bus, starting_place=a, destination=b, time=c, price=d)
        Route.objects.bulk_create(obj_list)

        return HttpResponse(obj_list)
