from django.forms import ModelForm

from application.models import Application, Profile

class ApplicationForm(ModelForm):
    required_css_class = 'label-required'
    
    class Meta:
        model = Application
        fields = ['num_hackathons', 'cool_project', 'last_summer', 'anything_else']
        labels = {
            "num_hackathons": "How many hackathons have you attended?",
            "cool_project": "Describe a cool project that you've made.",
            "last_summer": "What did you do last summer?",
            "anything_else": "Do you have anything else to tell us?"
        }
        
class ProfileForm(ModelForm):
    required_css_class = 'label-required'
    
    class Meta:
        model = Profile
        fields = [
            'name', 'school', 'zip_code',
            'github_profile', 'linkedin_profile', 'devpost_profile',
            'personal_website', 'dietary_restrictions', 't_shirt_size'
        ]