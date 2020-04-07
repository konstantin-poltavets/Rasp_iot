from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .serializers import mqttSerializer, gazSerializer
from rest_framework import filters, generics
from .models import mqtt, gazoline, orbi_tmp
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render_to_response
from qsstats import QuerySetStats
from datetime import date
from .forms import MyForm, gazForm, orbiForm
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Count, Value, Avg, Sum,  Min, Max
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models.functions import Extract
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .script import stock ,orbitrack, orbi_stop
from time import gmtime, strftime


class GazListjson(generics.ListAPIView):
    queryset=gazoline.objects.all().filter(fuel_type = 'LPG')
    serializer_class = gazSerializer




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

class gazListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = gazoline
    fields = '__all__'
   # paginate_by = 3views.indicator_mqtt


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
        date = POST['datepicker']
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
    queryset_temp = mqtt.objects.all().filter(topic = "home/poliv/temp")[::]
    queryset_hum = mqtt.objects.all().filter(topic = "home/poliv/water").order_by('-created_date')

    return render(request, "line_chart.html", {"my_data_temp": queryset_temp, "my_data_hum": queryset_hum})


def google_graphs(request):
    return render_to_response('graph1.html')

#@csrf_exempt
def google_rest_int(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        mqtt_data = mqtt.objects.all().filter(payload__lte =  22.5).filter(topic = "home/poliv/temp")
        serializer = mqttSerializer(mqtt_data, many=True)
        return JsonResponse(serializer.data, safe=False)




def google_rest(request):
        return render_to_response('test2020.html')


def indicator(request):
    return render_to_response('indicator_2.html')


def indicator_mqtt(request):
    orbitrack.main()
    return render_to_response('indicator_mqtt.html')

def orbiStop(request):
    orbi_stop.main()
    return render_to_response('index_1.html')


class gazDetailView(generic.DetailView):
    """Generic class-based list view for a list of authors."""
    model = gazoline

def gaz_add(request):
    if request.method == "POST":
        form = gazForm(request.POST, request.FILES)
        if form.is_valid():
            boards = form.save(commit=False)
            #modules.name = form['name'].value()
            boards.save()
            return redirect('gaz_list')
    else:
        form = gazForm()
    return render(request, 'myhome_1/gazoline_add.html', {'form': form})



def gaz_template(request):
    start_date = 2012
    end_date = 2013
    start_date = int(request.GET['year_1'])
    end_date = int(request.GET['year_2'])

    cont = gazoline.agregates(gazoline, start_date, end_date)
   # print(cont)

    values_count = [t["query_Count"] for t in cont]
    values_dat = [t["start_date"][:4] for t in cont]
    values_sum = [t["query_Sum"] for t in cont]
    values_avg = [t["query_Avg"] for t in cont]
    values_liters = [t["query_Liters"] for t in cont]
    values_rashod = [t["rashod"] for t in cont]
    values_distance = [t["distance"] for t in cont]

    values_count.pop(), values_dat.pop(),values_sum.pop()
    values_avg.pop(), values_liters.pop(), values_distance.pop(), values_rashod.pop()


    #print("disc", gazoline().disc())
   # print("values_dat", values_dat)
    #captions_a = [t[0].year for t in values_dat]

    return render(request, 'template_gaz_func.html', {'cont': cont,
                                                      'values_dat': values_dat,
                                                      'values_count': values_count,
                                                      'values_sum': values_sum,
                                                      'values_avg': values_avg,
                                                      'values_liters': values_liters,
                                                      'values_distance': values_distance,
                                                      'values_rashod': values_rashod
                                                      })







def gazoline_edit(request, pk):
    g = get_object_or_404(gazoline, pk=pk)
    if request.method == "POST":
        form = gazForm(request.POST,  request.FILES, instance=g)
        if form.is_valid():
            form.save()
            return redirect('gazoline_edit_view', pk=pk)
    else:
        form = gazForm(instance=g)
    return render(request, 'myhome_1/gazoline_edit.html', {'form': form})


def gaz_template_month(request):
    start_date = date(int(request.GET['year_1'][0:4]),1,1)
    end_date = date(int(request.GET['year_1'][0:4]),12,31)
    query = gazoline.objects.all()
    qsstats = QuerySetStats(query, date_field='created_date', aggregate=Sum('price_after_disc'))
    values = qsstats.time_series(start_date, end_date, interval='months')
    qsstats = QuerySetStats(query, date_field='created_date', aggregate=Sum('liters'))
    liters = qsstats.time_series(start_date, end_date, interval='months')
    query_1 = query.filter(created_date__year=start_date.year)

    return render_to_response( 'template_gaz_google.html', {'query':query_1,'values':values, 'liters':liters})





def gaz_search(request):
    return render_to_response('gaz_search.html')

def gchart(request):
    return render_to_response('gchart_1.html')


def gaz_search_result(request):

    start_date = date(int(request.GET['year_1']),1,1)
    end_date = date(int(request.GET['year_2']),12,31)

    query = gazoline.objects.all().filter(created_date__range=(start_date, end_date))
    query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
    query_Count = query.aggregate(Count('created_date'))["created_date__count"]
    query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
    query_Liters = query.aggregate(Sum('liters'))["liters__sum"]
    query_Min = query.aggregate(Min('millage'))["millage__min"]
    query_Max = query.aggregate(Max('millage'))["millage__max"]
    distance = query_Max - query_Min

    qsstats = QuerySetStats(query, date_field='created_date')
    values_dat_m = qsstats.time_series(start_date, end_date, interval='months', aggregate=Sum('price_after_disc'))
    values_a = [t[1] for t in values_dat_m]
    captions_a = [t[0] for t in values_dat_m]

    return render(request, 'search_result_gaz.html', {'values': values_dat_m,
                                                     'query_Avg': query_Avg,
                                                     'query_Count': query_Count,
                                                     'query_Sum': query_Sum,
                                                      'query_Liters': query_Liters,
                                                     'values_dat': values_dat_m,
                                                     'values_a': values_a,
                                                     'captions_a': captions_a,
                                                      'distance': distance })











class GazDelete(DeleteView):
    model = gazoline
   # template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('gaz_list')





class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


 #   line_chart = TemplateView.as_view(template_name='line_chart.html')
#    line_chart_json = LineChartJSONView.as_view()





import csv

from django.http import HttpResponse, request
from django.contrib.auth.models import User

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myhome_1_gazoline.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'created_date','fuel_type', 'liters','millage','price_after_disc','price_liter','station'])

    gaz = gazoline.objects.all().values_list( 'id', 'created_date','fuel_type', 'liters','millage','price_after_disc','price_liter','station')
    for gaz in gaz:
        writer.writerow(gaz)

    return response


def export_orbitrack_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myhome_1_orbitrack.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'distance', 'time', 'speed', 'created'])

    orbi = orbi_tmp.objects.all().values_list( 'id', 'distance', 'time', 'speed', 'created')
    for orbi in orbi:
        writer.writerow(orbi)

    return response


def get_success_url(self):
    return request.META.get('HTTP_REFERER')


def get_stock(request):
    start_date = date(2016, 3, 12)
    end_date = date(2016, 3, 16)

    stock_info = stock.main()

    return render_to_response( 'stock.html', { 'stock_info': stock_info})


def sec(request):

    secunds =  (strftime("%H:%M:%S", gmtime()))
    #orbitrack = orbitrack
    return HttpResponse(secunds)

class orbi_tmpListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = orbi_tmp
    fields = '__all__'
