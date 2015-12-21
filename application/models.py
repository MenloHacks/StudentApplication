from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Application(models.Model):
    NUM_HACKATHONS_CHOICES = (
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4+", "4+"),
    )
    
    profile = models.OneToOneField('Profile', related_name="application")
    num_hackathons = models.CharField(max_length=2, choices=NUM_HACKATHONS_CHOICES)
    cool_project = models.TextField()
    last_summer = models.TextField()
    anything_else = models.TextField()
    
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
    
    user = models.OneToOneField(User, related_name="profile")
    
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=150)
    zip_code = models.IntegerField()
    
    github_profile = models.URLField()
    linkedin_profile = models.URLField()
    devpost_profile = models.URLField()
    personal_website = models.URLField()
    dietary_restrictions = models.CharField(max_length=15, choices=DIETARY_RESTRICTIONS)
    t_shirt_size = models.CharField(max_length=2, choices=T_SHIRT_SIZES)