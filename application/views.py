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
import os


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
    
@login_required
def index_waiting(request):
    return render(request, "application/waiting.html", {})

@login_required
def index_result(request):
    try:
        app = request.user.application
    except Exception as e:
        if str(e) == "User has no application.":
            return render(request, "application/error_no_app.html", {})
        else:
            raise Exception(str(e))
    if app.admitted == True:
        if app.sanitized_school != "Other":
            others = Application.objects.filter(sanitized_school=app.sanitized_school, admitted=True)
        else:
            others = None
        print others
        return render(request, "application/result_yes.html", {"others":others, "url_len":len(app.form_url)})
    elif app.waitlisted == True:
        return render(request, "application/result_wait.html", {})
    else:
        return render(request, "application/result_no.html", {})
    
@login_required
def coming(request):
    app = request.user.application
    if request.GET.get("yes") == "1":
        app.can_come = True
        app.cannot_come = False
        app.save()
    elif request.GET.get("yes") == "0":
        app.cannot_come = True
        app.can_come = False
        app.save()
    elif request.GET.get("reset") == "1":
        app.cannot_come = False
        app.can_come = False
        app.save()
    return redirect("application:index")

@login_required
def upload(request):
    app = request.user.application
    if request.GET.get("url") != None:
        app.form_url = request.GET["url"]
        app.save()
    return redirect("application:index")

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


import csv, codecs, cStringIO
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([str(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def csv_export(request):
    if request.GET.get("p") == os.environ.get("CSV_PASSWORD"):
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
        writer = UnicodeWriter(response)#csv.writer(response)
        writer.writerow(data[0].keys())
        for entry in data:
            try:
                writer.writerow(entry.values())
            except UnicodeEncodeError as e:
                print str(e)
        return response
    else:
        return HttpResponse("no")