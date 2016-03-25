from django.shortcuts import render
import subprocess

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from TREC.forms import *
from TREC.models import *

import unicodedata

def homepage(request):
    return render(request, 'TRECapp/index.html', {})

def about(request):
    return render(request, 'TRECapp/about.html', {})

def leaderboard(request):
    return render(request, 'TRECapp/leaderboard.html',{})

@login_required
def editprofile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    # Check to see if HTTP POST, in order to manipulate data
    if request.method == 'POST':

        # Get data (in this case just the username)
        user_form = UpdateUserForm(request.POST, instance=user)

        # Get the rest of the data (everything but username, see forms.py)
        profile_form = UpdateUserProfileForm(request.POST, instance=profile)

        # If both forms are valid..
        if user_form.is_valid() and profile_form.is_valid():

            # Then save data in db
            user.save()

            # Check for profile picture
            if 'profilePic' in request.FILES:
                profile.profilePic = request.FILES['profilePic']

            # Save rest of user profile data
            profile.save()

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
    allRunsDesc = Run.objects.filter(task__title=task.title).order_by('-overall')
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
        rank = calculateRank(run, relevant_task)
        context_dict['run'] = run
        context_dict['task'] = relevant_task
        context_dict['track'] = relevant_track
        context_dict['rank'] = rank
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

@login_required
def submit(request):

    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        
        if form.is_valid():
            #name and run file should be saved to run now but we still need to give it a task and researcher
            run = form.save(commit=False)
            task = request.POST.get('task')
            taskObj = Task.objects.get(title=task)
            researcher = request.user
            run.task = taskObj
            run.researcher = researcher
            name = request.POST.get('name')
            filename = run.run_file.path
            judgement = taskObj.judgement_file.path
            #filename = str(run.run_file)
            print judgement
            print filename
            run.save()
            process = subprocess.Popen(['.trec_eval', judgement, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
            #judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
            #command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/trec_eval -c " + judgement + " " + filename
            #print "command = " + command + "\n"
            #output = subprocess.check_output([command],shell=True)
            outputList = process.split('\n')
            for lines in outputList:
                if "map" in lines:
                    line = lines.split("\t")
                    map = float(line[2])
                if "P10" in lines and p10 == "nothing":
                    line = lines.split("\t")
                    p10 = float(line[2])
	        if "P20" in lines and p20 == "nothing":
                    line = lines.split("\t")
                    p20 = float(line[2])
            print type(output)
            print "\n"
            print output
            print map
            print "\t"
            print p10
            print "\t"
            print p20
            run.mean_average_precision = map
            run.p10 = p10
            run.p20 = p20
            if map is not None:
                run.save()
                print run.run_file
                return HttpResponseRedirect('/TRECapp/')
            run.delete()
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
