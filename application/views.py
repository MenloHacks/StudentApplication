from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core import serializers
from django.conf import settings

from django.contrib.auth.decorators import login_required

from .forms import ApplicationForm, ProfileForm
from .models import User, Profile, Application, ApplicationReview
from registration.backends.hmac.views import RegistrationView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from django.contrib.auth.views import login
from registration.backends.hmac.views import ActivationView
from forms import ResendEmailForm
import json
import csv


try:
    SCHOOLS = json.dumps(json.load(open("static/school_names.json")))
except:
    SCHOOLS = json.dumps(json.load(open("PycharmProjects/StudentApplication/static/school_names.json")))
DIETARY_RESTRICTIONS = json.dumps([
    {"value": "None",
     "text": "None"},
    {"value": "Vegetarian",
     "text": "Vegetarian"},
    {"value": "Vegan",
     "text": "Vegan"},
    {"value": "Gluten Free",
     "text": "Gluten Free"},
    ])
emails = set()

dirpath = os.path.dirname(__file__)
filepath = os.path.join(dirpath, 'static/output2.csv')

try:
    with open("static/output2.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            emails.add(row[1])
except:
    with open(filepath) as f:
        reader = csv.reader(f)
        for row in reader:
            emails.add(row[1])

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)





class CustomRegistrationView(RegistrationView):
    """
    Register a new (inactive) user account, generate an activation key
    and email it to the user.

    This is different from the model-based activation workflow in that
    the activation key is simply the username, signed using Django's
    TimestampSigner, with HMAC verification on activation.

    """
    email_body_template_html = 'registration/activation_email.html'
    email_subject_template = 'registration/activation_email_subject.txt'

    def get_success_url(self, user):
        if user.email in emails:
            return ('login', (), {})
        return ('registration_complete', (), {})

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is simply the
        username, signed using TimestampSigner.
        """
        activation_key = self.get_activation_key(user)
        if user.email in emails:
            activation = ActivationView()
            activation.activate(activation_key=activation_key)
        else:
            context = self.get_email_context(activation_key)
            context.update({
                'user': user
            })
            subject = render_to_string(self.email_subject_template,
                                       context)
            # Force subject to a single line to avoid header-injection
            # issues.
            html_content = render_to_string(CustomRegistrationView.email_body_template_html,
                                            context)
            text_content = strip_tags(html_content)

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content,
                                         settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()



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
            others = Application.objects.filter(sanitized_school=app.sanitized_school, admitted=True, cannot_come=False)
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

@login_required
def bring_chaperone(request):
    if request.GET.get("bring") == "yes":
        request.user.application.can_bring_chaperone = True
    elif request.GET.get("bring") == "no":
        request.user.application.can_bring_chaperone = False
    request.user.application.save()
    return HttpResponse(request.GET.get("bring"))
    #return redirect("application:index")

# Create your views here.u
class Index(LoginRequiredMixin, View):
    guaranteed_admittance = ["Menlo School"]

    def get(self, request, prof_form=None, app_form=None):
        is_menlo = str("menloschool.org" in request.user.email).lower()
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
                return render(
                    request,
                    "application/profile.html",
                    {'prof_form': prof_form,
                     "ismenlo": is_menlo,
                     "schools": SCHOOLS,
                     "dietary_restrictions": DIETARY_RESTRICTIONS}
                )
        try:
            school = request.user.profile.school
        except:
            school = None
        if not is_submitted:
            if not app_form:
                try:
                    app_form = ApplicationForm(instance=request.user.application)
                except Exception:
                    app_form = ApplicationForm()
            return render(
                request,
                "application/application.html",
                {'prof_form': prof_form, 'app_form': app_form,
                 "ismenlo": str(school in
                                Index.guaranteed_admittance).lower(),
                 "api_key": settings.FILESTACK_API_KEY,
                 "is_menlo_django": school in
                                Index.guaranteed_admittance}
            )
        else:
            return render(request, "application/applied.html",
                          {'prof_form':prof_form,
                           "schools": SCHOOLS,
                           "dietary_restrictions": DIETARY_RESTRICTIONS
                           })
    
    def post(self, request):
        prof_form = ProfileForm(request.POST)
        valid = True
        app_form = ApplicationForm(request.POST)
        if prof_form.is_valid():
            existing_profile = True
            try:
                request.user.profile.delete()
            except Exception:
                existing_profile = False
            try:
                if prof_form.has_tried:
                    valid = False
            except:
                prof_form.has_tried = True
            new_prof = prof_form.save(commit=False)
            new_prof.user = request.user
            new_prof.save()
            if new_prof.school in Index.guaranteed_admittance and not existing_profile:
                return redirect('application:index')
            else:
                if app_form.is_valid():
                    try:
                        if request.user.application.submitted == True:
                            return redirect('application:index')
                        request.user.application.delete()
                    except Exception:
                        pass
                    new_app = app_form.save(commit=False)
                    new_app.user = request.user
                    if request.POST.get("submit") == "true":
                        Index.send_email(request.user)
                        new_app.submitted = True
                    new_app.save()
                    return redirect('application:index')
                else:
                    if valid:
                        return redirect('application:index')
                    else:
                        return self.get(request, prof_form=prof_form,
                                        app_form=app_form)
        else:
            prof_form = request.user.profile
            try:
                if app_form.is_valid():
                    try:
                        if request.user.application.submitted == True:
                            return redirect('application:index')
                        request.user.application.delete()
                    except Exception:
                        pass
                    new_app = app_form.save(commit=False)
                    new_app.user = request.user
                    if request.POST.get("submit") == "true":
                        Index.send_email(request.user)
                        new_app.submitted = True
                    new_app.save()
                    return redirect('application:index')
                else:
                    if valid:
                        return redirect('application:index')
                    else:
                        return self.get(request, prof_form=prof_form,
                                        app_form=app_form)
            except:
                pass
            return self.get(request, prof_form=prof_form, app_form=app_form)

    @staticmethod
    def send_email(user):
        first_name = user.profile.name.split(" ")[0]
        context = {
            "user": user,
            "name": first_name
        }
        if user.profile.school in Index.guaranteed_admittance:
            subject = "Thank you for registering for MenloHacks!"
            html_content = render_to_string(
                "registration/registered_email.html",
                context)
            text_content = strip_tags(html_content)

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content,
                                         settings.DEFAULT_FROM_EMAIL,
                                         [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        else:
            subject = "Thank you for applying for MenloHacks!"
            html_content = render_to_string(
                "registration/applied_email.html",
                context)
            text_content = strip_tags(html_content)

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content,
                                         settings.DEFAULT_FROM_EMAIL,
                                         [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    @staticmethod
    def get_prof(request, prof_form=None, app_form=None):
        is_menlo = str("menloschool.org" in request.user.email).lower()
        if request.POST:
            new_prof_form = ProfileForm(request.POST)
            if new_prof_form.is_valid():
                try:
                    request.user.profile.delete()
                except Exception:
                    pass
                new_prof = new_prof_form.save(commit=False)
                new_prof.user = request.user
                new_prof.save()
                return redirect("application:index")
        if not prof_form:
            try:
                prof_form = ProfileForm(instance=request.user.profile)
            except Exception:
                prof_form = ProfileForm()
        return render(
            request,
            "application/profile.html",
            {'prof_form': prof_form,
             "ismenlo": is_menlo,
             "schools": SCHOOLS,
             "dietary_restrictions": DIETARY_RESTRICTIONS
             }
        )
        
        
def profile_redirect(request):
    return redirect('application:index')

def redirecting_login(request):
    return login(request, redirect_authenticated_user=True)

class ResendEmail(CustomRegistrationView, ActivationView):

    def get(self, request, invalid=False):
        return render(request, "registration/resend_email.html",
                      {"invalid": invalid, "form": ResendEmailForm()})

    def post(self, request):
        form = ResendEmailForm(request.POST)
        user = self.get_user(form.data["username"])
        if user:
            self.send_activation_email(user)
            return render(request, "registration/registration_complete.html")
        else:
            return self.get(request, invalid=True)

def is_active(request):
    username = request.POST.get("username")
    activation_view = ActivationView()
    user = activation_view.get_user(username)
    if user:
        return HttpResponse("false")
    else:
        return HttpResponse("true")

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

#application view

#consider application review to have started if we've already reviewed some. Otherwise
#this will be false (this is reset on boot)
APPLICATION_REVIEW_ENABLED = ApplicationReview.objects.count() > 0


@login_required
def toggle_review(request):
    global APPLICATION_REVIEW_ENABLED
    if(request.user.is_staff):
        if request.GET.get('enabled') == 'yes' and APPLICATION_REVIEW_ENABLED == False:
            APPLICATION_REVIEW_ENABLED = True
            assign_reviewers()
        elif request.GET.get('enabled') == 'no' and APPLICATION_REVIEW_ENABLED == True:
            APPLICATION_REVIEW_ENABLED = False
        else:
            return JsonResponse({'error' : 'invalid parameter values'}, status=500)
    else:
        return HttpResponse(status=403)

from random import shuffle
def assign_reviewers():
    NUM_REVIEWERS_PER_APPLICATION = 3

    reviewers = User.objects.all().filter(is_staff=True)
    profiles = Profile.objects.all().exclude(school='Menlo School')

    reviewer_list = []
    for reviewer in reviewers:
        reviewer_list.append(reviewer)

    for profile in profiles:
        shuffle(reviewer_list)
        for i in xrange(0, NUM_REVIEWERS_PER_APPLICATION):
            profile.application_reviewers.add(reviewer_list[i])

        profile.save()

        if profile.user.application is None:
            profile.user.application = Application()
            profile.user.save()


def score_apps():
    pass


class ApplicationReviewManagerView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            return render(request, "review/enter_app_review.html", {'review_enabled' : APPLICATION_REVIEW_ENABLED})
        else:
            return render(request, "review/permissions_denied.html", {})



class ApplicationReviewView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_staff:
            if APPLICATION_REVIEW_ENABLED:
                #get review
                pass
            else:
                return render(request, "review/review_disabled.html", {})

        else:
            return render(request, "review/permissions_denied.html", {})
            #show a permissions denied view.

        pass

    def post(self, ):
        #save the review
        pass