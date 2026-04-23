from django.shortcuts import render
from .models import Book
from datetime import date


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date', 'name')
    context = {'books': books}
    return render(request, template, context)


def books_by_date(request, year, month, day):
    template = 'books/books_by_date.html'
    current_date = date(year, month, day)
    
    # Получаем книги за текущую дату
    books = Book.objects.filter(pub_date=current_date).order_by('name')
    
    # Находим предыдущую и следующую даты
    previous_date = Book.objects.filter(pub_date__lt=current_date)\
                                 .order_by('-pub_date')\
                                 .values_list('pub_date', flat=True)\
                                 .first()
    
    next_date = Book.objects.filter(pub_date__gt=current_date)\
                             .order_by('pub_date')\
                             .values_list('pub_date', flat=True)\
                             .first()
    
    context = {
        'books': books,
        'current_date': current_date,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, template, context)