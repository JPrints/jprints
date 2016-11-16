import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jprints.settings')

import django
django.setup()

from elasticsearch import Elasticsearch
from core.elastic_search import initialise_elastic_search
from django.contrib.auth.models import User
from core.models import Person, Role, Permission
from publications.models import Publication

def populate_publications():

    test_pubs = [
        {
         "depositor": "admin",
         "status": "I",
         "publication_type": "A",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Article 1",
         "abstract": "An abstract for Article 1",
         "subject": "1",
         "divisions": "1",
         },
         {
         "depositor": "admin",
         "status": "I",
         "publication_type": "A",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Article 2",
         "abstract": "An abstract for Article 2",
         "subject": "1",
         "divisions": "1",
         },
         {
         "depositor": "admin",
         "status": "I",
         "publication_type": "A",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Article 3",
         "abstract": "An abstract for Article 3",
         "subject": "1",
         "divisions": "1",
         },
         {
         "depositor": "test1",
         "status": "I",
         "publication_type": "S",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Book Section 1 (One)",
         "abstract": "An abstract for Book Section One, note that One is also a family name",
         "subject": "1",
         "divisions": "1",
         },
         {
         "depositor": "test2",
         "status": "I",
         "publication_type": "B",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Book Section 2",
         "abstract": "An abstract for Book Section 2",
         "subject": "1",
         "divisions": "1",
         },
         {
         "depositor": "test3",
         "status": "I",
         "publication_type": "B",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Book 1",
         "abstract": "An abstract for Book 1",
         "subject": "1",
         "divisions": "1",
         },
   
   ]

    for pub in test_pubs:
        add_publication(pub)

def add_publication(pub):
    print("add publication: depositor {0} type {1} title {2}".format(str(pub["depositor"]), str(pub["publication_type"]), str(pub["title"])))
    u = User.objects.get_or_create(username=pub["depositor"])[0]
    person = Person.objects.get_or_create(user=u)[0]
    #print("add_publication called person", person.id,  "user", u.id )
    p = Publication.objects.get_or_create(depositor=person, title=pub["title"])[0]
    p.status = pub["status"]
    p.publication_type = pub["publication_type"]
    p.publication_status = pub["publication_status"]
    p.visibility_status = pub["visibility_status"]
    p.abstract = pub["abstract"]
    p.subject = pub["subject"]
    p.divisions = pub["divisions"]
    p.save()


def populate_people():

    test_users = [
        {"username": "admin",
         "email": "pjw@drserv.org",
         "first": "Peter",
         "last": "West",
         "staff": "Yes",
         "disp_title": "Mr",
         "disp_given": "Peter",
         "disp_family": "West",
         "lang": "EN",
         "orcid": "0000-0002-0244-9026",
         "user_type": "Ad",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         },
    
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
         {"username": "test3",
         "email": "test@test3.com",
         "first": "Test",
         "last": "Three",
         "staff": "No",
         "disp_title": "Mr",
         "disp_given": "dispgiven",
         "disp_family": "",
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
    print("add user: {0} {1} {2}".format(str(user["username"]), str(user["first"]), str(user["last"])))
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


def clear_database():
    publications = Publication.objects.order_by('id')
    for publication in publications:
        print("About to delete publication ",publication.id,publication.title)
        publication.delete()

    users = User.objects.order_by('id')
    for user in users:
        if user.is_staff != True:
            print("deleting user ", user.id, user.last_name, user.is_staff)
            user.delete()

    people = Person.objects.order_by('id')
    for person in people:
        if person.user_type != "Ad":
            print("deleting person ",person.id,person.disp_family)
            person.delete()


if __name__ == '__main__':
    print("clear database")
    clear_database()

    print("Setup Elastic Search indexes")
    initialise_elastic_search()

    print("Start populate JPrints")
    populate_people()
    populate_publications()
    print("Finished JPrints population script")
