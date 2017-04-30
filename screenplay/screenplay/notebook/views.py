from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from datetime import datetime
from .models import ScreenPlay


def index(request):
    screenplay_list = ScreenPlay.objects.all()
    return render(request, 'home.html', {'post_list': screenplay_list})
