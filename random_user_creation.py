from application.models import *
import random
import string

def random_word(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

for i in xrange(0,100):
    username = random_word(10)

    user = User.objects.create_user(username=username, email=username, password='123')
    user.save()

    profile = Profile()

    profile.zip_code = 12345
    profile.user = user

    r = random.random()

    if r > 0.5:
        profile.devpost_profile = 'http://devpost.com/example'

    r = random.random()

    if r > 0.5:
        profile.linkedin_profile = 'https://linkedin.com/in/example'

    r = random.random()

    if r > 0.5:
        profile.github_profile = 'https://github.com/example'

    r = random.random()

    if r > 0.85:
        profile.is_campus_rep = True


    profile.save()

    r = random.random()

    if r > 0.2:
        app = Application()

        app.cool_project = random_word(500)
        app.last_summer = random_word(250)

        r = random.random()

        if r > 0.5:
            app.anything_else = random_word(250)

        r = random.random()

        if r > 0.5:
            app.anything_else = random_word(250)

        r = random.random()

        if r > 0.5:
            app.form_url = 'http://example.com'

        r = random.random()

        if r > 0.5:
            app.photo_form_url = 'http://example.com'

        app.user = user

        app.save()

    






