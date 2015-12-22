from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth.decorators import login_required

from .forms import ApplicationForm, ProfileForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

# Create your views here.
class Index(LoginRequiredMixin, View):
    def get(self, request, prof_form=None, app_form=None):
        if not prof_form:
            try:
                prof_form = ProfileForm(instance=request.user.profile)
            except Exception:
                prof_form = ProfileForm()
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
                request.user.application.delete()
            except Exception:
                pass
            new_app = app_form.save(commit=False)
            new_app.user = request.user
            new_app.save()
            return redirect('application:index')
        else:
            return self.get(request, prof_form=prof_form, app_form=app_form)
        
        
def profile_redirect(request):
    return redirect('application:index')