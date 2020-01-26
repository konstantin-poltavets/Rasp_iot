from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from libs.status import *
 

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"
    
    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)



@login_required(login_url='/accounts/login/') 
def index(request):
    return render(request, 'index_1.html')

def logout_view(request):
    logout(request)
    return render(request, 'index_1.html')



@login_required(login_url='/accounts/login/') 
def first(request):
    return render(request, 'first.html')


def pi_status(request):
    data = status_all()
    return render(request, 'pi_status.html', {"context" : data})
