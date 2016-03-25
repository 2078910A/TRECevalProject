import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TRECappProject.settings')

import django
django.setup()

from TREC.models import *

import random

def populate():
    user_bob = add_user("Bob", "bob")
    add_userprofile(user=user_bob, display_name="bob", organisation="Glasgow Uni")
    user_steve = add_user("Steve", "steve")
    add_userprofile(user_steve, display_name="steve", organisation="Stirling Uni")
    user_david = add_user("David", "david")
    add_userprofile(user_david, display_name="david", organisation="Falkirk Uni")
    user_john = add_user("John", "john")
    add_userprofile(user_john, display_name="john", organisation="Edinburgh")

    clinicalTrack = add_track("Clinical Decision Support", "https://clinical.com", description="Clinical searching...", genre="Medical")
    federatedWebTrack = add_track("Federated Web Seach", "https://fedWeb.com", description="Search the federated web", genre="Web")
    kbaTrack = add_track("Knowledge Base Acceleration", "https://kbaweb.com", description="Accelerate Knowledge Base",genre="Web")

    task1 = add_task(track=kbaTrack, title="KBA Track 1", task_url="https://twitter.com", description="A description of KBA Track 1", year=2005)
    task2 = add_task(track=federatedWebTrack, title="FW Track 1", task_url="https://steve.com", description="A description of FW Track 1", year=2001)
    task3 = add_task(track=clinicalTrack, title="Clinical Track 1", task_url="https://task3.com", description="A description of Clinical Track 1", year=2006)
    task4 = add_task(track=kbaTrack, title="KBA Track 2", task_url="https://task4.com", description="A description of KBA track 2", year=2005)
    #task5 = add_task(federatedWebTrak, "")

def add_user(username, password):
    u = User.objects.get_or_create(username=username)[0]
    u.username = username
    u.password = password
    u.save()
    return u

def add_userprofile(user, display_name, organisation, profilePic=None, email="", website="", aboutme=""):
    up = UserProfile.objects.get_or_create(user=user)[0]
    up.display_name = display_name
    up.organisation = organisation
    up.save()
    return up

def add_track(title, track_url, description, genre):
    t = Track.objects.get_or_create(title=title)[0]
    t.track_url = track_url
    t.description = description
    t.genre = genre
    t.save()
    return t

def add_task(track, title, task_url, description, year):
    t = Task.objects.get_or_create(title=title,track=track)[0]
    t.title = title
    t.task_url = task_url
    t.description = description
    t.year = year
    t.save()
    return t

def add_run(task, researcher, name):
    r = Run.objects.get_or_create(name=name)[0]
    r.researcher = researcher
    r.name = name
    r.run_type = random.choice(['MA','AU'])
    r.feedback_type = random.choice(['NO','PS','RE','OT'])
    r.query_type = random.choice(['TI', 'TD', 'DE', 'AL', 'OT'])
    r.p10 = random()
    r.p20 = random()
    r.mean_average_precision = random()
    r.save()
    return r

if __name__ == '__main__':
    print "starting population script..."
    populate()
