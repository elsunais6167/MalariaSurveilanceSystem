from django.shortcuts import render

# Create your views here.
def index(request):

    context = {

    }

    return render(request, 'index.html', context)

def station(request):

    context = {

    }

    return render(request, 'station.html', context)