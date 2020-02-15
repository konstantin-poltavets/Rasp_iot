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