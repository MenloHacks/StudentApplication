import psycopg2
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date, timedelta
import pickle



def send_reminder_emails():
    try:
        past_emails = pickle.load(open("/Users/thomaswoodside/PycharmProjects/StudentApplication/static"
        "/emails_sent.pkl"))
    except:
        past_emails = {}
    last_week = date.today() - timedelta(weeks=1)
    conn = psycopg2.connect("<database_url_>")
    cur = conn.cursor()
    cur.execute("""
    SELECT email,name,school from auth_user
    FULL JOIN application_application
    ON auth_user.id=application_application.user_id
    FULL JOIN application_profile
    ON auth_user.id=application_profile.user_id
    WHERE (submitted IS NULL
    OR submitted <> TRUE)
    AND date_joined < %(last_week)s
    """, {"last_week": last_week})
    results = cur.fetchall()
    for result in results:
        email = result[0]
        if email in past_emails:
            if past_emails[email] < last_week:
                past_emails[email] = date.today()
                send_email(result)
        else:
            send_email(result)
            past_emails[email] = date.today()
    pickle.dump(past_emails, open(
        "/Users/thomaswoodside/PycharmProjects/StudentApplication/static"
        "/emails_sent.pkl", "w"))

def send_email(info):
    email_address, name, school = info
    menlo = False
    displayname = ""
    if school == "Menlo School":
        menlo = True
    if "@menloschool.org" in email_address:
        menlo = True
    if name:
        displayname = " " + name.split(" ")[0]
    print(menlo, displayname)

    context = {
        "name": displayname,
        "menlo": menlo
    }
    if menlo:
       subject = "Finish registering for MenloHacks!"
    else:
        subject = "Finish applying to MenloHacks!"
    html_content = render_to_string("registration/reminder_email.html",
                                    context)
    text_content = strip_tags(html_content)

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content,
                                 settings.DEFAULT_FROM_EMAIL,
                                 [email_address])
    msg.attach_alternative(html_content, "text/html")
    msg.send()