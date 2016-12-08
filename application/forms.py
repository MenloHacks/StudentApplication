from django.forms import ModelForm, Select
from django_select2.forms import Select2Mixin

from application.models import Application, Profile

class ApplicationForm(ModelForm):
    required_css_class = 'label-required'
    
    class Meta:
        model = Application
        fields = ['num_hackathons', 'cool_project', 'last_summer',
                  'anything_else']
        labels = {
            "num_hackathons": "How many hackathons have you attended?",
            "cool_project": "Describe a cool project that you've made.",
            "last_summer": "What did you do last summer?",
            "anything_else": "Do you have anything else to tell us?"
        }

"""
Overwritten classes that don't cut off at spaces and only
allow one input.
"""
class Select2TagMixin(object):
    """Mixin to add select2 tag functionality."""

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Add select2's tag attributes."""
        self.attrs.setdefault('data-tags', 'true')
        return super(Select2TagMixin, self).build_attrs(extra_attrs, **kwargs)


class Select2TagWidget(Select2TagMixin, Select2Mixin, Select):
    """
    Select2 drop in widget for for tagging.

    Example for :class:`.django.contrib.postgres.fields.ArrayField`::

        class MyWidget(Select2TagWidget):

            def value_from_datadict(self, data, files, name):
                values = super(MyWidget, self).value_from_datadict(data, files, name):
                return ",".join(values)
    """

    pass



class ProfileForm(ModelForm):
    required_css_class = 'label-required'
    
    class Meta:
        model = Profile
        fields = [
            'name', 'school', 'zip_code', 'phone_number', 'gender',
            'dietary_restrictions', 't_shirt_size', 'github_profile',
            'linkedin_profile', 'devpost_profile', 'personal_website',
            'form_url'
        ]
        widgets = {
            "school": Select2TagWidget,
            "dietary_restrictions": Select2TagWidget
        }
        
        labels = {"zip_code":"School ZIP code", "form_url": "form", "name":
            "Full Name"}