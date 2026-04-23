from django.shortcuts import render
from .models import Article


def articles_list(request):
    template = 'articles/news.html'
        
    articles = Article.objects.all().order_by('-published_at').prefetch_related('scopes__tag')
    
    context = {
        'object_list': articles,
    }

    return render(request, template, context)