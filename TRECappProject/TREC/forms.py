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

class UpdateUserProfileForm(forms.ModelForm):
        class Meta:
                model = UserProfile
                fields = ('profilePic','email','website','display_name','organisation','aboutme')

class UpdateUserForm(forms.ModelForm):
        class Meta:
                model = User
                fields = ('username',)


class LeaderboardForm(forms.Form):

    track_choices = [('', '---Choose a Track---')]
    for track in Track.objects.all():
        track_choices += [(track, track)]
    track = forms.ChoiceField(choices=track_choices, label='Track', widget=forms.Select(attrs={'id': 'track-selector'}))

    task_choices = [('', '---Choose a Task---')]
    for task in Task.objects.all():
        task_choices += [(task.title, task.title)]
    task = forms.ChoiceField(choices=task_choices, label='Task', widget=forms.Select(attrs={'id': 'task-selector'}))

    result_type_choices = [
        ('', '---Sort by---'),
        ('mean_average_precision', 'map'),
        ('p10', 'p10'),
        ('p20', 'p20'),
        ]
    result_type = forms.ChoiceField(choices=result_type_choices, label='Sort by', widget=forms.Select(attrs={'id': 'sortby-selector'}))



    #On reflection, this seems like a weird idea. Just display 12 entries on the leaderboard,
    #fills the page nicer.
    #run_choices = [
    #    (5, '5'),
    #    (10, '10'),
    #    (20, '20'),
    #    ]
    #num_of_runs = forms.ChoiceField(choices=run_choices, label='Number of runs: ')

#class SubmitForm(forms.Form):

#    track_choices = [('', '---Choose a Track---')]
#    for track in Track.objects.all():
#        track_choices += [(track.title, track.title)]
#    track = forms.ChoiceField(choices=track_choices, label='Select Track')

#    task_choices = [('', '---Choose a Task---')]
#    for task in Task.objects.all():
#        task_choices += [(task.title, task.title)]
#    task = forms.ChoiceField(choices=task_choices, label='Select Task')
#
#    name = forms.CharField(max_length = 4)
#
#    run = forms.FileField()

class SubmitForm(forms.ModelForm):

    track_choices = [('', '---Choose a Track---')]
    for track in Track.objects.all():
        track_choices += [(track.title, track.title)]
    track = forms.ChoiceField(choices=track_choices, label='Select Track')

    task_choices = [('', '---Choose a Task---')]
    for task in Task.objects.all():
        task_choices += [(task.title, task.title)]
    task = forms.ChoiceField(choices=task_choices, label='Select Task')

    class Meta:
        model = Run
        fields = ['name', 'run_file']

    def __init__(self, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': 'Enter a 4 digit unique ID for your run'})