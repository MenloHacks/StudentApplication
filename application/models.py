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

    cumulative_score = models.FloatField(default=0)


    def __str__(self):
        return "App for %s (%s)" % (
            self.user.username,
            "done" if self.submitted else "in-progress"
        )

class DoNotKillMeForNotValidating(models.CharField):
    pass


class Profile(models.Model):

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



    user = models.OneToOneField(User, related_name="profile")

    name = models.CharField(max_length=100)
    school = models.CharField(max_length=150)
    zip_regex = RegexValidator(regex="^\d{5}$",
                                message="Zip code must be in the format "
                                        "'94027'. Only five numeric digits "
                                        "allowed.")
    zip_code = models.IntegerField(validators=[zip_regex])

    phone_regex = RegexValidator(regex=r'^(?:\([2-9]\d{2}\)\ ?|[2-9]\d{2}(?:\-?|\ ?))[2-9]\d{2}[- ]?\d{4}$',
                                 message="You must enter a valid US phone "
                                         "number.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex])

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male")


    github_profile = models.URLField(blank=True, default="https://github.com/")
    linkedin_profile = models.URLField(blank=True, default="https://www.linkedin.com/in/")
    devpost_profile = models.URLField(blank=True, default="http://devpost.com/")
    personal_website = models.CharField(max_length=200, blank=True, default="http://")
    dietary_restrictions = models.CharField(max_length=150, default="None")
    t_shirt_size = models.CharField(max_length=2, choices=T_SHIRT_SIZES, default="XS")
    is_campus_rep = models.BooleanField(default=False)


    auto_accept = models.BooleanField(default=False)
    application_reviewers = models.ManyToManyField("self", blank=True)


    def __str__(self):
        return "%s (%s)" % (self.name, self.user.username)



class ApplicationReview(models.Model):
    profile = models.OneToOneField(Profile, related_name="profile_reviewed", blank=True)

    reviewer = models.OneToOneField(User, related_name="reviewer", null=True)

    passion_score = models.IntegerField(default=0)
    experience_score = models.IntegerField(default=0)

    adjusted_passion_score = models.FloatField(default=0)
    adjusted_experience_score = models.FloatField(default=0)

