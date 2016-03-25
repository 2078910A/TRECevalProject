import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TRECappProject.settings')

import django
django.setup()

from TREC.models import *

import random

def populate():
    user_bob = add_user("Bob", "bob")
    bobprofile = add_userprofile(user_bob, "https://gla.ac.uk", display_name="bob", organisation="Glasgow Uni")
    user_steve = add_user("Steve", "steve")
    steveprofile = add_userprofile(user_steve, "https://gla.ac.uk", display_name="steve", organisation="Stirling Uni")
    user_david = add_user("David", "david")
    davidprofile = add_userprofile(user_david, "https://gla.ac.uk", display_name="david", organisation="Falkirk Uni")
    user_john = add_user("John", "john")
    johnprofile = add_profile(user_john, "https://Si.ac.uk", display_name="john", organisation="Edinburgh")

    clinicalTrack = add_track("Clinical Decision Support", "https://clinical.com", description="Clinical searching...")
    federatedWebTrack = add_track("Federated Web Seach", "https://fedWeb.com", description="Search the federated web")
    kbaTrack = add_track("Knowledge Base Acceleration", "https://kbaweb.com", description="Accelerate Knowledge Base")

    task1 = add_task(kbaTrack, "KBA Track 1", "https://twitter.com", "A description of KBA Track 1")
    task2 = add_task(federatedWedTrack, "FW Track 1", "https://steve.com", "A description of FW Track 1")
    task3 = add_task(clinicalTrack, "Clinical Track 1", "https://task3.com", "A description of Clinical Track 1")
    task4 = add_task(kbaTrack, "KBA Track 2", "https://task4.com", "A description of KBA track 2")
    #task5 = add_task(federatedWebTrak, "")

def add_user(username, password):
    u = User.objects.get_or_create(username=username)[0]
    u.username = username
    u.password = password
    u.save()
    return u

def add_userprofile(user, website, display_name, organisation):
    up = UserProfile.objects.get_or_create(user=user)
    up.website = website
    up.display_name = display_name
    up.organisation = organisation
    up.save()
    return up

def add_track(title, track_url, description):
    t = Track.objects.get_or_create(title=title)
    t.track_url = track_url
    t.description = description
    t.genre = random.choice(['NE','WE','ME','BL','LE','OT'])
    t.save()
    return t

def add_task(track, title, task_url, description, year):
    t = Task.objects.get_or_create(title=title)
    t.track = track
    t.title = title
    t.task_url = task_url
    t.description = description
    t.year = year
    t.save()
    return t

def add_run(task, researcher, name):
    r = Run.objects.get_or_create(name=name)
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