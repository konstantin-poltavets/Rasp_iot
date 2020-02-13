from django.shortcuts import render, redirect
from django.views import generic
from .serializers import mqttSerializer
from rest_framework import filters, generics
from .models import mqtt, gaz
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render_to_response
from qsstats import QuerySetStats
from datetime import date
from .forms import MyForm, gazForm
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Count, Value



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
    model = gaz
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
    model = gaz

def gaz_add(request):
    if request.method == "POST":
        form = gazForm(request.POST, request.FILES)
        if form.is_valid():
            boards = form.save(commit=False)
            #modules.name = form['name'].value()
            boards.save()
            return redirect('myhome_1/gaz_detail', pk=boards.pk)
    else:
        form = gazForm()
    return render(request, 'myhome_1/gaz_add.html', {'form': form})



def gaz_template(request):

    query = gaz.objects.all()
    #q2 = query.cost

    return render(request, 'template_gaz.html', {'values':query})