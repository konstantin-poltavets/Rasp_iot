from django.shortcuts import render, redirect
from .serializers import mqttSerializer
from rest_framework import filters, generics
from .models import mqtt, Payment
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from qsstats import QuerySetStats
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Avg, Count
from django.template import RequestContext
import calendar
from datetime import datetime
import datetime
from .forms import MyForm


class mqttList(generics.ListAPIView):
    queryset = mqtt.objects.all()
    serializer_class = mqttSerializer


class mqttDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = mqtt.objects.all()
    serializer_class = mqttSerializer


class mqttViewSet(viewsets.ModelViewSet):
    __basic_fields = ('topic','payload','created_date',)
    #queryset = mqtt.objects.all().filter(topic = "temp")
    queryset = mqtt.objects.all()
    serializer_class = mqttSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = __basic_fields
    search_fields = __basic_fields




def graph_1(request):
    return render(request, 'graph1.html')

def publish_1(request):
    return render(request, 'publish.html')

def select(request):
    queryset = mqtt.objects.all().filter(topic = "temperature")[::0]
    #queryset = mqtt.objects.get(Q(topic = "home/bath/esp1/humidity"))
    return render(request, "select.html", {"mqtt": queryset})


def search(request):
    return render_to_response('search.html')


def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']

    if 'r' in request.GET and request.GET['r']:
        r = int(request.GET['r'])

        queryset = mqtt.objects.filter(topic = q)[::r]
        return render_to_response('search_result.html',
            {'mqtt': queryset, 'query': q, 'skipped_rows': r})
    else:
        return HttpResponse('Please submit a search term.')


def publish(request):
    if request.method == "POST":
        queryset_temp = mqtt.objects.all().filter(topic = "temperature")[::0]
        queryset_hum = mqtt.objects.all().filter(topic = "humidity")[::0]
        date=POST['datepicker']
        return render(request.POST, "line_chart.html", {"my_date": date, "my_data_temp": queryset_temp, "my_data_hum": queryset_hum})
    else:
        form = MyForm()
        return render(request, 'calendar_2.html', {'form': form})


def view_func_iii(request):
    start_date = date(2016, 3, 12)
    end_date = date(2016, 3, 16)

    queryset = mqtt.objects.all()
    qsstats = QuerySetStats(queryset, date_field='created_date')
    values = qsstats.time_series(start_date, end_date, interval='days', aggregate=Count('created_date'))
    summary = qsstats.time_series(start_date, end_date,  aggregate=Count('payload'))

    return render_to_response('template_2.html', {'values': values, 'summary': summary})


def view_func(request):
    queryset_temp = mqtt.objects.all().filter(topic = "home/poliv/temp")[::100]
    queryset_hum = mqtt.objects.all().filter(topic = "home/poliv/water")[::100]

    return render(request, "line_chart.html", {"my_data_temp": queryset_temp, "my_data_hum": queryset_hum})


def google_graphs(request):
    return render_to_response('graph1.html')

def google_rest(request):
    mqtt_data = mqtt.objects.all().filter(topic = "home/poliv/temp")[::100]
    serialized = mqttSerializer(mqtt_data.topic)
    print (serialized.data)
    return render(request, 'google_rest.html', serialized.data)