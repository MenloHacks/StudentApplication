from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core import serializers

from django.contrib.auth.decorators import login_required

from .forms import ApplicationForm, ProfileForm
from .models import Application

import json
import csv
import io


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

# Create your views here.
class Index(LoginRequiredMixin, View):
    def get(self, request, prof_form=None, app_form=None):
        is_submitted = False
        try:
            is_submitted = request.user.application.submitted
        except Exception:
            pass
        
        if not prof_form:
            try:
                prof_form = ProfileForm(instance=request.user.profile)
            except Exception:
                prof_form = ProfileForm()
        
        if not is_submitted:
            if not app_form:
                try:
                    app_form = ApplicationForm(instance=request.user.application)
                except Exception:
                    app_form = ApplicationForm()
            return render(
                request,
                "application/index.html",
                {'prof_form':prof_form, 'app_form':app_form}
            )
        else:
            return render(request, "application/applied.html", {'prof_form':prof_form})
    
    def post(self, request):
        prof_form = ProfileForm(request.POST)
        app_form = ApplicationForm(request.POST)
        if prof_form.is_valid() and app_form.is_valid():
            try:
                request.user.profile.delete()
            except Exception:
                pass
            new_prof = prof_form.save(commit=False)
            new_prof.user = request.user
            new_prof.save()
            
            try:
                if request.user.application.submitted == True:
                    return redirect('application:index')
                request.user.application.delete()
            except Exception:
                pass
            new_app = app_form.save(commit=False)
            new_app.user = request.user
            if request.POST.get("submit") == "true":
                new_app.submitted = True
            new_app.save()
            return redirect('application:index')
        else:
            return self.get(request, prof_form=prof_form, app_form=app_form)
        
        
def profile_redirect(request):
    return redirect('application:index')

def csv_export(request):
    data_string = serializers.serialize("json", Application.objects.all())
    data = json.loads(data_string)
    
    for i in range(0, len(data)):
        entry = data[i]
        profile = Application.objects.get(pk=entry["pk"]).user.profile
        profile_data_string = serializers.serialize("json", [profile])
        profile_data = json.loads(profile_data_string)
        
        data[i] = dict(entry["fields"].items() + profile_data[0]["fields"].items())
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="menlohacks-export.csv"'
    writer = csv.writer(response)
    writer.writerow(data[0].keys())
    for entry in data:
        try:
            writer.writerow(entry.values())
        except UnicodeEncodeError:
            pass
    return response