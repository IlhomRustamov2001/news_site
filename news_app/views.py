from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.db.models import Q
from hitcount.views import HitCountDetailView
from hitcount.views import HitCountMixin

from hitcount.utils import get_hitcount_model


def news_list(request):
    #new_list=News.objects.filter(status=News.Status.Published)
    news_list=News.published.all()
    context={
        'news_list':news_list
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, news):
    news=get_object_or_404(News, slug=news, status=News.Status.Published)
    context={}
    hit_count=get_hitcount_model().objects.get_for_object(news)
    hits=hit_count.hits
    hitcontext=context['hitcount'] = {'pk':hit_count.pk}
    #hitcontext={'pk':hit_count.pk}
    #context['hitcount']=hitcontext
    hit_count_mixin=HitCountMixin
    hit_count_response = hit_count_mixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits+=1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits


    comments=news.comments.filter(active=True)
    comment_count=comments.count()

    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.news=news
            #izooh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user=request.user
            #malumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form=CommentForm()
    else:
        comment_form=CommentForm()
    context={
        'news':news, 
        'new_comment':new_comment,
        'comments':comments,
        'comment_form':comment_form,
        'comment_count':comment_count
    }
    return render(request, 'news/news_detail.html', context)

class NewsDetailView(DetailView, FormView):
    model=News
    template_name='news/news_detail.html'
    context_object_name='news'
    form_class=CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


    

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

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model=News
    fields=('title', 'body', 'image', 'category', 'status')
    template_name='crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model=News
    template_name='crud/news_delete.html'
    success_url=reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model=News
    template_name='crud/news_create.html'
    fields=('title', "title_ru", "title_uz", "title_eng", 'slug', 'body', "body_uz", "body_en", "body_ru", 'image', 'category', 'status')


@login_required   
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users=User.objects.filter(is_superuser=True)
    context={
        'admin_users':admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsList(ListView):
    model=News
    template_name='news/search_result.html'
    context_object_name='barcha_yangiliklar'

    def get_queryset(self) :
        query=self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
