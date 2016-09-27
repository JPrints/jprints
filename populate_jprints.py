import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jprints.settings')

import django
django.setup()

from django.contrib.auth.models import User
from core.models import Person, Role, Permission

def populate():
    print("populate called")


    test_users = [
        {"username": "test1",
         "email": "test@test1.com",
         "first": "Test",
         "last": "One",
         "staff": "No",
         "disp_title": "Mr",
         "disp_given": "Test",
         "disp_family": "One",
         "lang": "EN",
         "orcid": "1234-1234-1234-1234",
         "user_type": "Us",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         },
         {"username": "test2",
         "email": "test@test2.com",
         "first": "Test",
         "last": "Two",
         "staff": "No",
         "disp_title": "Mr",
         "disp_given": "Test",
         "disp_family": "Two",
         "lang": "DE",
         "orcid": "0000-1234-0002-0002",
         "user_type": "Us",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         },
 
    ]

    for user in test_users:
        add_user(user)

def add_user(user):
    print("add_user called")
    print("user: {0} {1} {2}".format(str(user["username"]), str(user["first"]), str(user["last"])))
    u = User.objects.get_or_create(username=user["username"], email=user["email"], first_name=user["first"], last_name=user["last"])[0]
    p = Person.objects.get_or_create(user=u)[0]
    p.disp_title = user["disp_title"]
    p.disp_given = user["disp_given"]
    p.disp_family = user["disp_family"]
    p.lang = user["lang"]
    p.orcid = user["orcid"]
    p.user_type = user["user_type"]
    p.dept = user["dept"]
    p.org = user["org"]
    p.addr = user["addr"]
    p.save()


if __name__ == '__main__':
    print("Start JPrints population script")
    populate()
    print("Finished JPrints population script")
