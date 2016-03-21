from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from TREC.forms import LeaderboardForm
from TREC.models import *

import unicodedata

def homepage(request):
    return render(request, 'TRECapp/index.html', {})

def about(request):
    return render(request, 'TRECapp/about.html', {})

def leaderboard(request):
    return render(request, 'TRECapp/leaderboard.html',{})
	
def profile(request):
    return render(request, 'TRECapp/profile.html',{})

def submit(request):
    return render(request, 'TRECapp/submit.html',{})
	
from TREC.forms import UserForm, UserProfileForm

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
			
	
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'TRECapp/login.html', {})


def leaderboard(request):

    context_dict = {}

    #Check if we've been sent a form to process data from
    if request.method == 'POST':
        form = LeaderboardForm(request.POST)
        print "method is post"
        #Can't see why the form wouldn't be valid as it's all drop down menus, but is_valid
        #initialises the cleaned_data dictionary
        if form.is_valid():
            #This is the result type we want to sort runs by
            sort_attribute = form.cleaned_data['result_type']
            #This is the track that we want to see runs from
            search_track = form.cleaned_data['track']
            taskSearchedFor = form.cleaned_data['task']
            #Search for the runs which have been submitted to the task the user has selected and
            #order them by the attribute the user selected
            top_runs = Run.objects.filter(task__title=taskSearchedFor).order_by('-' + sort_attribute)[:10]

            context_dict['top_runs'] = top_runs

    #Haven't been sent a form so render one for the user
    else:
        form = LeaderboardForm()

    context_dict['form'] = form

    return render(request, 'TRECapp/leaderboard.html', context_dict)

def ajax_task_request(request):

    if request.method == 'GET':

        #This will hold a value which is the TITLE of the track the user just selected
        track = request.GET.get('selected_track')
        #Use the title to get the actual object from the db
        trackObj = Track.objects.get(title=track)
        #Use this track object to get a list of all the tasks associated with it
        taskList = list(Task.objects.filter(track=trackObj))

        taskTitles = []

        for task in taskList:
            #The task title is returned in unicode, so turn it into a string. Not the
            #task.title parameter in the .normalize() function.
            taskTitleString = unicodedata.normalize('NFKD', task.title).encode('ascii', 'ignore')
            taskTitles = taskTitles + [task.title]

        return render(request, 'TRECapp/relevant-tasks.html', { 'taskTitles': taskTitles })

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
	
from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/TRECapp/')
