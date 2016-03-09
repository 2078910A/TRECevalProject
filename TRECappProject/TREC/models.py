from django.db import models
from django.contrib.auth.models import User

#A helper function which returns the UNIX path where the user's
#profile pic is to be stored in the media directory
def user_profilepic_directory_path(instance, filename):
    #stores uploaded profile pics to 'media/profile_pics/user_<id>/filename'
    return '/profile_pics/user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    email = models.EmailField()
    profilePic = models.ImageField(upload_to=user_profilepic_directory_path)
    website = models.URLField(blank=True)
    display_name = models.CharField(max_length=50)
    organisation = models.CharField(max_length=50)

class Track(models.Model):

    title = models.CharField(max_length=64, unique=True)
    track_url = models.URLField(blank=True)
    description = models.CharField(max_length=256)

    NEWS = 'N'
    WEB = 'W'
    BLOG = 'B'
    MEDICAL = 'M'
    LEGAL = 'L'

    GENRE_CHOICES = (
        (NEWS, 'News'),
        (WEB, 'Web'),

        )

    genre = models.CharField(max_length=2, choice=GENRE_CHOICES, blank=False)

class Task(models.Model):

    track = models.ForeignKey(Track)
    title = models.CharField(max_length=60)
    task_url = models.URLField(blank=True)
    description = models.CharField(max_length=256)
    year = models.IntegerField()

    #Will store judgement (.qrel) files in 'media/judgements/'
    judgement_file = models.FileField(upload_to='judgements/')
