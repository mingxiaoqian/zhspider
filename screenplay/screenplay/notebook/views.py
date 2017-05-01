from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from .models import ScreenPlay

# Create your views here.

def index(request):
    limit = 32
    screenplay_count = ScreenPlay.objects.all().count()
    screenplay_list = ScreenPlay.objects.all()
    paginator = Paginator(screenplay_list, limit)

    page = request.GET.get('page')  # 获取页码
    try:
        screenplay_list = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        screenplay_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        screenplay_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    query_params = request.GET.copy()
    query_params.pop('page', None)
    context = {
        'post_count': screenplay_count,
        'page': page,
        'paginator': paginator,
        'query_params': query_params,
        'post_list': screenplay_list,
    }

    return render(request, 'home.html', context)
