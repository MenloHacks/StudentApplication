from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import pickle

# Create your models here.


class Application(models.Model):
    NUM_HACKATHONS_CHOICES = (
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4+", "4+"),
    )
    
    user = models.OneToOneField(User, related_name="application")
    num_hackathons = models.CharField(
        max_length=2,
        choices=NUM_HACKATHONS_CHOICES, default="0"
    )
    cool_project = models.TextField(blank=True)
    last_summer = models.TextField(blank=True)
    anything_else = models.TextField(blank=True)
    form_url = models.CharField(max_length=200, null=True, blank=True)
    photo_form_url = models.CharField(max_length=200, null=True, blank=True)

    submitted = models.BooleanField(default=False)
    
    admitted = models.BooleanField(default=False)
    waitlisted = models.BooleanField(default=False)
    
    sanitized_school = models.CharField(max_length=100, default="Other")
    
    can_come = models.BooleanField(default=False)
    cannot_come = models.BooleanField(default=False)
    
    can_bring_chaperone = models.NullBooleanField(default=None)

    
    def __str__(self):
        return "App for %s (%s)" % (
            self.user.username, 
            "done" if self.submitted else "in-progress"
        )
    
class Profile(models.Model):
    DIETARY_RESTRICTIONS = (
        ("None", "None"),
        ("Vegetarian", "Vegetarian"),
        ("Vegan", "Vegan"),
        ("Gluten Free", "Gluten Free"),
    )
    
    T_SHIRT_SIZES = (
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
    )
    
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("No answer", "Prefer not to say"),
    )

    SCHOOLS = pickle.load(open("static/school_list.pkl", "rb"))

    
    user = models.OneToOneField(User, related_name="profile")
    
    name = models.CharField(max_length=100)
    school = models.CharField(choices=SCHOOLS, max_length=150)
    zip_code = models.IntegerField()
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male")

    
    github_profile = models.URLField(blank=True, default="https://github.com/")
    linkedin_profile = models.URLField(blank=True, default="https://www.linkedin.com/in/")
    devpost_profile = models.URLField(blank=True, default="http://devpost.com/")
    personal_website = models.CharField(max_length=200, blank=True, default="http://")
    dietary_restrictions = models.CharField(max_length=15, choices=DIETARY_RESTRICTIONS, default="None")
    t_shirt_size = models.CharField(max_length=2, choices=T_SHIRT_SIZES, default="XS")

    application_reviewers = models.ManyToManyField("self", blank=True)


    def __str__(self):
        return "%s (%s)" % (self.name, self.user.username)

class ApplicationReview(models.Model):
    profile = models.OneToOneField(User, related_name="profile")

    score = models.IntegerField()
    adjusted_score = models.FloatField()
