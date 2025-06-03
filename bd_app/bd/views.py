from django.shortcuts import render, redirect
from .models import Application,Type_TC
from .forms import ApplicationForm

def bd_watching(request):
    applications = Application.objects.order_by('date_of_accomplishment')
    return render(request,"bd/bd_watching.html", {'applications': applications})

def profile(request):
    return render(request, "bd/profile.html")

def create_order(request):
    error = ''
    if request.method == 'POST':
        form = ApplicationForm(request.POST)  # Заполняем форму данными из POST-запроса
        if form.is_valid():
            form.save()  # Сохраняем данные в базу данных
            
        else:
            error = 'Форма заполнена неверно!'
            data = {  # Передаем заполненную форму с ошибками в шаблон
                'form': form,
                'error': error
            }
            return render(request, 'bd/create_order.html', data)

    else:  # Если это GET-запрос
        form = ApplicationForm()  # Создаем пустую форму

    data = {
        'form': form,
        'error': error  # error может быть пустой строкой, если нет ошибок
    }
    return render(request, 'bd/create_order.html', data)

def type_tc_list(request):
    type_tc = Type_TC.objects.all()
    return render(request, 'bd/catalog.html',
                  context={'type_tc': type_tc})

def catalog(request):
    applications = Type_TC.objects.order_by('name_type_tc')
    return render(request,"bd/catalog.html")

