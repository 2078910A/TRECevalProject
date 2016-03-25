from django.shortcuts import render
import subprocess
import os

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from TREC.forms import *
from TREC.models import *

import unicodedata
import os

def homepage(request):
    return render(request, 'TRECapp/index.html', {})

def about(request):
    return render(request, 'TRECapp/about.html', {})

def leaderboard(request):
    return render(request, 'TRECapp/leaderboard.html',{})

@login_required
def editprofile(request):

    # Get user currently signed in
    user = request.user
    # Get the profile details of the user currently signed in
    profile = UserProfile.objects.get(user=user)

     # A boolean value for telling the template whether the profile edit was successful.
     # Set to False initially. Code changes value to True when profile edit succeeds.
    updated = False

    # Check to see if HTTP POST, in order to manipulate data
    if request.method == 'POST':

        # Get data (in this case just the username)
        user_form = UpdateUserForm(request.POST, instance=user)

        # Get the rest of the data (everything but username, see forms.py)
        profile_form = UpdateUserProfileForm(request.POST, instance=profile)

        # If both forms are valid..
        if user_form.is_valid() and profile_form.is_valid():

            #Saving both forms
            user_form.save()
            profile_form.save()

            # Then save user data in db
            user.save()

            # Check for profile picture
            if 'profilePic' in request.FILES:
                profile.profilePic = request.FILES['profilePic']

            # Save rest of user profile data
            profile.save()

            # Update our variable to tell the template profile edit was successful.
            updated = True

            # Redirect to the users profile
            return HttpResponseRedirect('/TRECapp/profile/')

    else:

        # Not HTTP POST..
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateUserProfileForm(instance=profile)

        # Render template
    return render(request, 'TRECapp/editprofile.html',
                  {'user_form': user_form, 'profile_form': profile_form})

@login_required	
def profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    ownRuns = Run.objects.filter(researcher=user)
    runTitles = []
    for run in ownRuns:
        runTitles += [run.name]
    return render(request, 'TRECapp/profile.html',{'profile': profile, 'runs': runTitles})

def calculateRank(run, task):
    allRunsDesc = Run.objects.filter(task__title=task.title).order_by('-mean_average_precision')
    rank = 1
    for otherRun in allRunsDesc:
        if run.name == otherRun.name:
            break
        rank += 1
    return rank

def ajax_profile_info_request(request):
    context_dict = {}
    if request.method == 'GET':
        selected_run = request.GET.get('selected_run')
        run = Run.objects.get(name=selected_run)
        relevant_task = run.task
        relevant_track = relevant_task.track
        print relevant_track
        rank = calculateRank(run, relevant_task)
        print rank
        context_dict['run'] = run
        context_dict['task'] = relevant_task
        context_dict['track'] = relevant_track
        context_dict['rank'] = rank
        print context_dict
        return render(request, 'TRECapp/profile-details-table.html', context_dict)


@login_required	
def otherprofile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        othersRuns = Run.objects.filter(researcher=user)
        runTitles = []
        for run in othersRuns:
            runTitles += [run.name]
        return render(request, 'TRECapp/profile.html',{'profile': profile, 'runs': runTitles})
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return HttpResponseRedirect('/TRECapp/')



from TREC.forms import UserForm, UserProfileForm

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

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
            if 'profilePic' in request.FILES:
                profile.profilePic = request.FILES['profilePic']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            # Sign the user in automatically and redirect to homepage
            user = authenticate(username=user.username,
                                password=user_form.cleaned_data['password'])
            login(request, user)

            return HttpResponseRedirect('/TRECapp/')

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
            'TRECapp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
			
	
def user_login(request):
     # Dictionary telling us, in case of login error, the nature of the error
    context = {}
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
                return HttpResponseRedirect('/TRECapp/')
            else:
                # An inactive account was used - no logging in!
                context['loginError'] = "Your TRECHub account is disabled."
        else:
            # Bad login details were provided. So we can't log the user in.
            context['loginError'] = "Your username and password do not match. Try again."


        # Passing context variables to display any errors to user

    return render(request, 'TRECapp/login.html', context)

import subprocess

@login_required
def submit(request):

    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)

        if form.is_valid():

            #name and run file should be saved to run now but we still need to give it a task, researcher, name and assign the relevant task to it
            run = form.save(commit=False)

            #Get the title of the task from the form, use this to pull the actual object from the db and assign this task to the submitted run
            task = request.POST.get('task')
            taskObj = Task.objects.get(title=task)
            run.task = taskObj

            #Of course, we need to also know who submitted the run, this is just taken from the request
            researcher = request.user
            run.researcher = researcher
            username = researcher.username

            #Get the 4 digit identifier for the run and assign it to it
            name = request.POST.get('name')
            run.name = name

            #We've given a value to the fields designated by the submit form, so we can save this into the db. This is necessary as we want access
            #to the run file itself when calling the trec_eval script
            run.save()

            #Use the task object to get the associated track object as we'll be needing to know where the qrels are and what the track slug is
            trackObj = taskObj.track
            judgement = taskObj.judgement_file
            judgementStr = str(judgement)

            #Run file is the actual run the user just submittied, it's a path structured like, "/runs/<track.slug>/<task.slug>/<filename>"
            #this directory structure won't change so if we split the string at every "/" and take the 4th element then we get the filename
            #that the user just submitted
            runFile = str(run.run_file)
            runFileName = runFile.split("/")[3]

            #We'll be using these slugs to construct the parameters for the call to trec_eval
            trackSlug = trackObj.slug
            taskSlug = taskObj.slug

            #Construct the command which is to be executed by the terminal and execute it
            command = "sudo ./trec_eval.8.1/trec_eval -c ./media/judgements/{0}/{1}.qrels ./media/runs/{2}/{3}/{4}".format(trackSlug, taskSlug, trackSlug, taskSlug, runFileName)
            os.system(command)

            #This is what's output to the terminal from trec_eval which we then split at every newline character to get a list of lines of output
            output = subprocess.check_output(command, shell=True)
            outputlist = output.split("\n")

            #This is so we don't pick up the p100, p1000 or p200 values by using a python string search (if "p10" in line:)
            p10 = None
            p20 = None

            #Get the p10, p20 and map results for the user's run
            for line in outputlist:
                if "map" in line:
                    line = line.split("\t")
                    mean_ap = float(line[2])
                if "P10" in line and p10 == None:
                    line = line.split("\t")
                    p10 = float(line[2])
                if "P20" in line and p20 == None:
                    line = line.split("\t")
                    p20 = float(line[2])

            #Assign these values to the run object that we've already saved and save it again so these fields are updated
            run.p10 = p10
            run.p20 = p20
            run.mean_average_precision = mean_ap
            run.save()

            print "This run's P10 is: " + str(run.p10) + "\n" + "This run's P20 is: " + str(run.p20) + "\n" + "This run's map is: " + str(run.mean_average_precision)
            return HttpResponseRedirect("/TRECapp/profile/")

    else:
        form = SubmitForm()
    return render(request, 'TRECapp/submit.html', {'form': form})

def leaderboard(request):

    context_dict = {}

    #Check if we've been sent a form to process data from
    if request.method == 'POST':
        form = LeaderboardForm(request.POST)
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

def ajax_track_task_info_request(request):

    context_dict = {}

    if request.method == 'GET':

        selected_track = request.GET.get('selected_track')
        selected_task = request.GET.get('selected_task')

        if selected_track:

            trackObj = Track.objects.get(title=selected_track)
            context_dict['track'] = trackObj
            template = 'TRECapp/dynamic-track-table.html'

        elif selected_task:

            taskObj = Task.objects.get(title=selected_task)
            context_dict['task'] = taskObj
            template = 'TRECapp/dynamic-task-table.html'

    return render(request, template, context_dict)


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
