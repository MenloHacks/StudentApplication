from django.forms import ModelForm

from application.models import Application

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['num_hackathons', 'cool_project', 'last_summer', 'anything_else']