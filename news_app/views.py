from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.views.generic import TemplateView, ListView

def news_list(request):
    #new_list=News.objects.filter(status=News.Status.Published)
    news_list=News.published.all()
    context={
        'news_list':news_list
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, news):
    news=get_object_or_404(News, slug=news, status=News.Status.Published)
    context={
        'news':news
    }
    return render(request, 'news/news_detail.html', context)

def homePageView(request):
    categories=Category.objects.all()
    news_list=News.published.all().order_by('-publish_time')[:5]
    local_one=News.published.filter(category__name='mahalliy')[:1]
    local_news=News.published.all().filter(category__name='mahalliy')[:5]
    context={
        'news_list':news_list,
        'categories':categories,
        'local_one':local_one,
        'local_news':local_news
    }
    return render(request, 'news/home.html', context)

class HomePageView(ListView):
    model=News
    template_name='news/home.html'
    context_object_name='news'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['mahalliy_habarlar'] = News.published.all().filter(category__name='mahalliy')[:5]
        context['xorij_habarlar'] = News.published.all().filter(category__name='xorij')[:5]
        context['sport_habarlar'] = News.published.all().filter(category__name='Sport')[:5]
        context['texnologiya_habarlar'] = News.published.all().filter(category__name='Texnologiya')[:5]



        return context

def wrongPage(request):
    context={

    }
    return render(request, 'news/404.html', context)

def aboutPage(request):
    context={

    }
    return render(request, 'news/about.html', context)

class ContactPageView(TemplateView):
    template_name='news/contact.html'
    def get(self, reqeust, *args, **kwargs):
        form=ContactForm()
        context={
            'form':form
        }
        return render(reqeust, 'news/contact.html', context)
    
    def post(self,request, *args, **kwargs):
        form=ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('<h2> biz bilan boglanganingiz uchun rahmat</h2>')
        context={
            'form':form
        }
        return render(request, 'news/contact.html', context )
    
class LocalNewsView(ListView):
    model=News
    template_name='news/mahalliy.html'
    context_object_name='mahalliy_yangiliklar'

    def get_queryset(self) :
        news=News.published.all().filter(category__name='mahalliy')
        return news

class ForeignNewsView(ListView):
    model=News
    template_name='news/xorij.html'
    context_object_name='xorij_yangiliklari'

    def get_queryset(self) :
        news=News.published.all().filter(category__name='xorij')
        return news

class TechnologyNewsView(ListView):
    model=News
    template_name='news/texnologiya.html'
    context_object_name='texnologik_yangiliklar'

    def get_queryset(self) :
        news=News.published.all().filter(category__name='Texnologiya')
        return news
    

class SportNewsView(ListView):
    model=News
    template_name='news/sport.html'
    context_object_name='sport_yangiliklari'

    def get_queryset(self) :
        news=News.published.all().filter(category__name='Sport')
        return news