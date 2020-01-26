from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .forms import ModulesForm, BoardsForm,  Mqtt, Mqttypes
from .models import Modules, Boards
from django.views import generic
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models.query import QuerySet


def index(request):
        # form = Modules.objects.all()
    return render(request, 'iot/map.html')


def modules_edit(request, pk):
    modules = get_object_or_404(Modules, pk=pk)
    if request.method == "POST":
        form = ModulesForm(request.POST,  request.FILES, instance=modules)
        if form.is_valid():
            form.save()
            return redirect('modules_edit', pk=pk)
    else:
        form = ModulesForm(instance=modules)
        #modules.name = form['photos'].value()
    return render(request, 'iot/modules_edit.html', {'form': form})


def modules_add(request):
    if request.method == "POST":
        form = ModulesForm(request.POST, request.FILES)
        if form.is_valid():
            modules = form.save(commit=False)
            #modules.name = form['name'].value()
            modules.save()
            return redirect('modules_edit', pk=modules.pk)
    else:
        form = ModulesForm()
    return render(request, 'iot/modules_add.html', {'form': form})


def modules_list(request):
    id = Modules.QuerySet.values_list('id')
    name = list(Modules.objects.values_list('name'))
    description = list(Modules.objects.values_list('description'))
    num_modules = Modules.objects.all().count()

    return render(request, 'iot/modules_list_orig.html', context=({"num_modules": num_modules,
                            "name": name, "id": id, "description": description}))


class ModulesListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Modules
    paginate_by = 3


class ModulesDetailView(generic.DetailView):
    """Generic class-based list view for a list of authors."""
    model = Modules


class BoardsListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Boards
    paginate_by = 3


def boards_edit(request, pk):
    boards = get_object_or_404(Boards, pk=pk)
    if request.method == "POST":
        form = BoardsForm(request.POST,  request.FILES, instance=boards)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Saved.')
            return redirect('boards_edit', pk=pk)

        else:
            messages.warning(request, 'Please correct the error.')
    else:
        form = BoardsForm(instance=boards)

    return render(request, 'iot/boards_edit.html', {'form': form})



def boards_add(request):
    if request.method == "POST":
        form = BoardsForm(request.POST, request.FILES)
        if form.is_valid():
            boards = form.save(commit=False)
            #modules.name = form['name'].value()
            boards.save()
            return redirect('boards_edit', pk=boards.pk)
    else:
        form = BoardsForm()
    return render(request, 'iot/boards_add.html', {'form': form})



def publish(request):

    return render(request, 'iot/publish.html')

#class auth_views.LoginView.as_view()


def linkedboards(request):
    if request.method == 'POST':
        modules_form = ModulesForm(request.POST)
        boards_form = BoardsForm(request.POST)

        if modules_form.is_valid() and boards_form.is_valid():
            modules_form.save()
            boards_form.save()
    else:
        modules_form = ModulesForm
        boards_form = BoardsForm
    return render(request, 'iot/linkedboards.html', context=({"modules_form": modules_form,
                            "boards_form": boards_form}))


class MqttListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Mqtt
    paginate_by = 3

class MqttypesListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Mqttypes
    paginate_by = 3

def publish(request):
   return render(request, 'iot/publish.html')