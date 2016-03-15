from django.db import models
from django.contrib.auth.models import User


#A helper function which returns the UNIX path where the user's
#profile pic is to be stored in the media directory.
def user_profilepic_directory_path(instance, filename):
    #stores uploaded profile pics to 'media/profile_pics/user_<id>/filename'
    return '/profile_pics/user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    profilePic = models.ImageField(upload_to=user_profilepic_directory_path)
    website = models.URLField(blank=True)
    display_name = models.CharField(max_length=50)
    organisation = models.CharField(max_length=50)

    def __unicode__(self):
        return "Username: {0}, Display name: {1}".format(self.user.username, self.display_name)


class Track(models.Model):

    title = models.CharField(max_length=50, unique=True)
    track_url = models.URLField(blank=True)
    description = models.CharField(max_length=100)

    GENRE_CHOICES = (
            ('NE', 'News'),
            ('WE', 'Web'),
            ('ME', 'Medical'),
            ('BL', 'Blog'),
            ('LE', 'Legal'),
        )

    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)

    def __unicode__(self):
        return self.title

#Returns a path of format 'judgements/<Track title>/task_<task id>/'
#This is where each judgement file will be stored
def task_judgement_file_path(instance):
    return 'judgements/{0}/task_{1}'.format(instance.track.title, instance.id)

class Task(models.Model):

    track = models.ForeignKey(Track)
    task_url = models.URLField(unique=True)
    description = models.CharField(max_length=256)
    year = models.IntegerField()

    #Will store judgement (.qrel) files in 'media/judgements/'
    judgement_file = models.FileField(upload_to=task_judgement_file_path)

    def __unicode__(self):
        return "Track: {0}, Task: {1}, Year: {2}".format(self.track,
                                                     self.description, self.year)


class Run(models.Model):

    task = models.ForeignKey(Task)
    researcher = models.ForeignKey(User)
    name = models.CharField(max_length=4, unique=True)

    RUN_CHOICES = (
            ('MA', 'Manual'),
            ('AU', 'Automatic'),
        )

    run_type = models.CharField(max_length=2, choices=RUN_CHOICES)

    FEEDBACK_CHOICES = (
            ('NO', 'None'),
            ('PS', 'Pseudo'),
            ('RE', 'Relevance'),
            ('OT', 'Other'),
        )

    feedback_type = models.CharField(max_length=2, choices=FEEDBACK_CHOICES)

    QUERY_CHOICES = (
            ('TI', 'Title'),
            ('TD', 'Title & Description'),
            ('DE', 'Description'),
            ('AL', 'All'),
            ('OT', 'Other'),
        )

    query_type = models.CharField(max_length=2, choices=QUERY_CHOICES)

    def __unicode__(self):
        return "Unique tag: {0}, Submitted by: {1}".format(self.name, self.researcher.username)