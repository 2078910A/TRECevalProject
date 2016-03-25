import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TRECappProject.settings')

import django
django.setup()
from django.core.files import File
from TRECappProject.settings import DATA_ROOT
from TREC.models import *

import random

def populate():
    user_jill = add_user("jill", "jill")
    add_userprofile(user=user_jill, display_name="jill", organisation="Glasgow Uni")
    user_bob = add_user("bob", "bob")
    add_userprofile(user_bob, display_name="bob", organisation="Stirling Uni")
    user_jen = add_user("jen", "jen")
    add_userprofile(user_jen, display_name="jen", organisation="Falkirk Uni")
    
    robust2005 = add_track("Robust2005", "http://trec.nist.gov/data/t14_robust.html", description="News Retrieval", genre="News")
    terabyte = add_track("Terabyte","http://www-nlpir.nist.gov/projects/terabyte/", description="Terabyte Web Track", genre="Web")
    apnews = add_track("AP News", "", description="News Retrieval Track",genre="News")

    task1 = add_task(track=robust2005, title="Robust2005", task_url="http://trec.nist.gov/data/t14_robust.html", description="For each topic find all the relevant documents", year=2005, judgement=os.path.join(DATA_ROOT,"robust","aq.trec2005.qrels"))
    task2 = add_task(track=terabyte, title="Web2005", task_url="http://www-nlpir.nist.gov/projects/terabyte/", description="Find all the relevant web pages", year=2005, judgement=os.path.join(DATA_ROOT,"web","dg.trec.qrels"))
    task3 = add_task(track=apnews, title="APNews", task_url="", description="Find all the relevant news articles", year=2001, judgement=os.path.join(DATA_ROOT,"news","ap.trec.qrels"))

def add_user(username, password):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(username)
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

def add_task(track, title, task_url, description, year, judgement):
    t = Task.objects.get_or_create(title=title,track=track)[0]
    t.title = title
    t.task_url = task_url
    t.description = description
    t.year = year
    if judgement:
        t.judgement_file = File(open(judgement))
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
