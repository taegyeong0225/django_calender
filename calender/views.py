from django.shortcuts import render

# Create your views here.
from calender.models import Events

def index(request):
    return render(request, 'index.html')