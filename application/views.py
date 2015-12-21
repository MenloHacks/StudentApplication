from django.shortcuts import render

from .forms import ApplicationForm, ProfileForm

# Create your views here.
def index(request):
    prof_form = ProfileForm()
    app_form = ApplicationForm()
    return render(request, "application/index.html", {'prof_form':prof_form, 'app_form':app_form})