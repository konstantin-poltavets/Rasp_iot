from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .serializers import mqttSerializer
from rest_framework import filters, generics
from .models import mqtt, gazoline
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render_to_response
from qsstats import QuerySetStats
from datetime import date
from .forms import MyForm, gazForm
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Count, Value, Avg, Sum
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models.functions import Extract
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView







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
   # paginate_by = 3


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
    queryset_temp = mqtt.objects.all().filter(topic = "home/poliv/temp")[::100]
    queryset_hum = mqtt.objects.all().filter(topic = "home/poliv/water")[::100]

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
    years = gazoline.objects.all()
    #query_Count = query.aggregate(Count('price_liter'))["price_liter__count"]
    #print(years.values("created_date__year")["created_date__year"])
    #query_year = years.aggregate(Count("created_date__year")).distinct('created_date__year')
    query_year = gazoline.objects.only('created_date').dates('created_date', 'year', order =  'DESC')
    #print(query_year.year)
    values_year = [t.year for t in query_year]
    #query = gazoline.objects.all().filter(created_date__year=values_year[0])
    #query_list = [q_l for q_l in gazoline.objects.all().filter(created_date__year=values_year[values_year]) ]
    #print(values_year)
    #print("------------------>>")
    #query_Sum = years.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]
    #print(query_Sum)
    query_list = [ gazoline.objects.all().filter(created_date__year = k) for k in values_year]
    #print(query_list)
    captions_m = ["Jan", "Feb", "March", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    #values_a = [1,2,3,4,5,6,7,8,9,10,11,12]
    #values_a = [gazoline.objects.all().filter(created_date__year=k) for k in values_year]

    start_date = date(2012, 1, 1)
    end_date = date(2020, 12, 31)
    query = gazoline.objects.all()
    query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
    query_Count = query.aggregate(Count('price_liter'))["price_liter__count"]
    query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]

    qsstats = QuerySetStats(query, date_field='created_date')

    values_dat = qsstats.time_series(start_date, end_date, interval='years', aggregate=Sum('price_after_disc'))
    values_a = [t[1] for t in values_dat]
    captions_a = [t[0].year for t in values_dat]

    values_dat_2012 = qsstats.time_series(start_date, end_date, interval='months', aggregate=Sum('price_after_disc'))
    values_a_2012 = [t[1] for t in values_dat_2012]
    print("values_a_2012: ", values_a_2012)
    captions_a_2012 = [t[0].month for t in values_dat_2012]
    print("captions_a_2012: ", captions_a_2012)

    return render(request, 'template_gaz.html', {'values_year': values_year,
                                                 'values': query_list,
                                                 'values_a': values_a,
                                                 'captions_a_2013': captions_a_2012[0:12],
                                                 'values_a_2012': values_a_2012[0:12],
                                                 'values_a_2013': values_a_2012[12:24],
                                                 'values_a_2014': values_a_2012[24:36],
                                                 'values_a_2015': values_a_2012[36:48],
                                                 'values_a_2016': values_a_2012[48:60],
                                                 'values_a_2017': values_a_2012[60:72],
                                                 'values_a_2018': values_a_2012[72:84],
                                                 'values_a_2019': values_a_2012[84:96],
                                                 'values_a_2020': values_a_2012[96:108]
                                                 })



"""""
    start_date = date(2012, 1, 1)
    end_date = date(2016, 12, 31)
    query = gazoline.objects.all()
    query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
    query_Count = query.aggregate(Count('price_liter'))["price_liter__count"]
    query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]


    qsstats = QuerySetStats(query, date_field='created_date')
    values_dat = qsstats.time_series(start_date, end_date, interval='years', aggregate=Sum('price_after_disc'))
    #summary = qsstats.time_series(start_date, end_date, aggregate=Count('payload'))
    values_a = [t[1] for t in values_dat]
    captions_a = [t[0].year for t in values_dat]
    

    return render(request, 'template_gaz.html', {'values':query ,
                                                 'query_Avg':query_Avg ,
                                                 'query_Count':query_Count,
                                                 'query_Sum':query_Sum,
                                                  'values_dat':values_dat,
                                                 'values_a':values_a,
                                                 'captions_a':captions_a})
"""""

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
    start_date = date(2012, 1, 1)
    end_date = date(2016, 12, 31)
    query = gazoline.objects.all()
    query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
    query_Count = query.aggregate(Count('price_liter'))["price_liter__count"]
    query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]


    qsstats = QuerySetStats(query, date_field='created_date')
    values_dat = qsstats.time_series(start_date, end_date, interval='years', aggregate=Sum('price_after_disc'))
    #summary = qsstats.time_series(start_date, end_date, aggregate=Count('payload'))
    values_a = [t[1] for t in values_dat]
    captions_a = [t[0].year for t in values_dat]


    return render(request, 'template_gaz.html', {'values':query ,
                                                 'query_Avg':query_Avg ,
                                                 'query_Count':query_Count,
                                                 'query_Sum':query_Sum,
                                                  'values_dat':values_dat,
                                                 'values_a':values_a,
                                                 'captions_a':captions_a})


def gaz_search(request):
    return render_to_response('gaz_search.html')


def search_result_gaz(request):

    start_date = date(int(request.GET['year_1']),1,1)
    end_date = date(int(request.GET['year_2']),12,31)

    query = gazoline.objects.all()
    query_Avg = query.aggregate(Avg('price_liter'))["price_liter__avg"]
    query_Count = query.aggregate(Count('price_liter'))["price_liter__count"]
    query_Sum = query.aggregate(Sum('price_after_disc'))["price_after_disc__sum"]

    qsstats = QuerySetStats(query, date_field='created_date')
    values_dat = qsstats.time_series(start_date, end_date, interval='years', aggregate=Sum('price_after_disc'))
    values_a = [t[1] for t in values_dat]
    captions_a = [t[0].year for t in values_dat]

    return render(request, 'template_gaz.html', {'values': query,
                                                     'query_Avg': query_Avg,
                                                     'query_Count': query_Count,
                                                     'query_Sum': query_Sum,
                                                     'values_dat': values_dat,
                                                     'values_a': values_a,
                                                     'captions_a': captions_a})










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


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()