from django.shortcuts import render


# Create your views here.

def metas(request):
	template='meta/metas.html'
	return render(request, template)

