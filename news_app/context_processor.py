from .models import *

def latest_news(request):
    latest_news=News.published.all().order_by('-publish_time')
    context={
        'latest_news':latest_news
    }
    return context