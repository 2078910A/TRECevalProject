from django import forms
from TREC.models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
                model = User
                fields = ('username','password')

class UserProfileForm(forms.ModelForm):

	class Meta:
                model = UserProfile
                fields = ('profilePic','email','website','display_name','organisation')


class LeaderboardForm(forms.Form):

    track_choices = []
    for track in Track.objects.all():
        track_choices += [(track, track)]
    track = forms.ChoiceField(choices=track_choices, label='Track', widget=forms.Select(attrs={'class': 'track-selector'}))

    task_choices = []
    for task in Task.objects.all():
        task_choices += [(task.title, task.title)]
    task = forms.ChoiceField(choices=task_choices, label='Task', widget=forms.Select(attrs={'class': 'task-selector'}))

    result_type_choices = [
        ('mean_average_precision', 'map'),
        ('p10', 'p10'),
        ('p20', 'p20'),
        ]
    result_type = forms.ChoiceField(choices=result_type_choices, label='Sort by', widget=forms.Select(attrs={'class': 'sortby-selector'}))


    #On reflection, this seems like a weird idea. Just display 12 entries on the leaderboard,
    #fills the page nicer.
    #run_choices = [
    #    (5, '5'),
    #    (10, '10'),
    #    (20, '20'),
    #    ]
    #num_of_runs = forms.ChoiceField(choices=run_choices, label='Number of runs: ')
