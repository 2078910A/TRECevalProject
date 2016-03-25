from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

#A helper function which returns the UNIX path where the user's
#profile pic is to be stored in the media directory.
def user_profilepic_directory_path(instance, filename):
    #stores uploaded profile pics to 'media/profile_pics/user_<id>/filename'
    return '/profile_pics/user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    profilePic = models.ImageField(upload_to='profile_pics', blank=True)
    email = models.EmailField(default="")
    website = models.URLField(default="",blank=True)
    display_name = models.CharField(max_length=50,default="")
    organisation = models.CharField(max_length=50,default="",blank=True)
    aboutme = models.TextField(max_length=1000,default="",blank=True)

    def grabPic(self):
        if self.profilePic:
            return self.profilePic.url
        else:
            return '/media/profile_pics/default.png'


    def __unicode__(self):
        return "Username: {0}, Display name: {1}".format(self.user.username, self.display_name)


class Track(models.Model):

    title = models.CharField(max_length=50, unique=True, default="")
    track_url = models.URLField(unique=True)
    description = models.CharField(max_length=100)
    slug = models.SlugField(default="")

    GENRE_CHOICES = (
            ('NE', 'News'),
            ('WE', 'Web'),
            ('ME', 'Medical'),
            ('BL', 'Blog'),
            ('LE', 'Legal'),
            ('OT', 'Other'),
        )

    genre = models.CharField(max_length=2, choices=GENRE_CHOICES)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Track, self).save(*args, **kwargs)

#Returns a path of format 'judgements/<Track title>/task_<task id>/'
#This is where each judgement file will be stored
def task_judgement_file_path(instance, filename):
    return 'judgements/{0}/{1}'.format(instance.track.slug, instance.slug)

class Task(models.Model):

    track = models.ForeignKey(Track)
    title = models.CharField(max_length=128, unique=True, default="")
    task_url = models.URLField()
    description = models.CharField(max_length=256)
    year = models.IntegerField(blank=False)
    slug = models.SlugField(default="")

    #Will store judgement (.qrel) files in 'media/judgements/'
    judgement_file = models.FileField(upload_to=task_judgement_file_path)

    def __unicode__(self):
        return "{0}, Track: {1}, Year: {2}".format(self.title,
                                                     self.track, self.year)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Task, self).save(*args, **kwargs)

def run_path(instance, filename):
    filename = "user_{0}".format(instance.researcher.username)
    return "runs/{0}/{1}/{2}".format(instance.task.track.slug, instance.task.slug, filename)


class Run(models.Model):

    task = models.ForeignKey(Task)
    researcher = models.ForeignKey(User)
    name = models.CharField(max_length=4, unique=True)
    run_file = models.FileField(upload_to=run_path)

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

    mean_average_precision = models.FloatField(blank=True, default=0.0)
    p10 = models.FloatField(blank=True, default=0.0)
    p20 = models.FloatField(blank=True, default=0.0)

    def __unicode__(self):
        return "{0}, Submitted by: {1}".format(self.name, self.researcher.username)
