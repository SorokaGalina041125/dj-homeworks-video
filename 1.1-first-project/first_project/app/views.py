from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.urls import reverse 
import datetime
import os


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time =  datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    msg = f'Текущее время: {formatted_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    files = os.listdir('.') 
    result = "<h1>Содержимое рабочей директории:</h1><ul>"
    for file in files:
        result += f"<li>{file}</li>"
    result += "</ul>"
    
    return HttpResponse(result)
    raise NotImplemented
