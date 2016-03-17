# Setup Django settings and models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menlohacks.settings")

import django
django.setup()

# Begin program
from django.contrib.auth.models import User

import json

f = open("result.json", "r")
data = json.loads(f.read())

for school, students in data.items():
    for student_id_str in students:
        student_id = int(student_id_str)
        student = User.objects.get(pk=student_id)
        print student.email
        student.application.admitted = True
        student.application.sanitized_school = school
        student.application.save()