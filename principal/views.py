from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
	return render(request, 'principal/index.html')

def home(request):
	return render(request, 'principal/home.html')

