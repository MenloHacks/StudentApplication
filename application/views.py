from django.shortcuts import render

from .forms import ApplicationForm

# Create your views here.
def index(request):
    form = ApplicationForm()
    return render(request, "application/index.html", {'form':form})