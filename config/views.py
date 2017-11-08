from django.shortcuts import render

def config(request):
    template = 'config/config.html'
    return render(request, template)
