from django.forms import ModelForm

from application.models import Application

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['num_hackathons', 'cool_project', 'last_summer', 'anything_else']
        labels = {
            "num_hackathons": "How many hackathons have you attended?",
            "cool_project": "Describe a cool project that you've made.",
            "last_summer": "What did you do last summer?",
            "anything_else": "Do you have anything else to tell us?"
        }