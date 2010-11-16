from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from diesel.fuel.models import AnnouncementForm, Announcement, UserProfileForm,\
    UserProfile, UserForm

def index(request):
    print request.user.is_authenticated()
    return render_to_response('index.html',
                              {'announcement_form':AnnouncementForm(),
                               'announcements': Announcement.objects.all()},
                              context_instance=RequestContext(request))

def diesellogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return index(request)
        else:
            return render_to_response('index.html', 
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', {"error_message":'Invalid Credentials',
                                                 'announcements': Announcement.objects.all()},
                                                 context_instance=RequestContext(request))

def diesellogout(request):
    if request.user is not None: 
        logout(request)
    return render_to_response('index.html', {"error_message":"Successfully Logged Out",
                                             'announcements': Announcement.objects.all()},
                                             context_instance=RequestContext(request))
    
@login_required
def addAnnouncement(request):
    form = AnnouncementForm(request.POST)
    announcement = form.save(commit=False)
    announcement.created_by = request.user
    announcement.save()
    return redirect("/fuel/")

@login_required
def userProfile(request):
    try:
        profile = request.user.get_profile()
        if profile.lucky_number:
            print 'Lucky number: ' + str(profile.lucky_number)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    return renderProfile(request, UserForm(instance=request.user), UserProfileForm(instance=profile))

@login_required
def renderProfile(request, user_form, profile_form, msg=None):
    if msg:
        return render_to_response('profile.html', {'message':msg,
                                                   'user_form':user_form,
                                                   'profile_form':profile_form,
                                                   'announcements': Announcement.objects.all()},
                                                   context_instance=RequestContext(request))
    else:
        return render_to_response('profile.html', {'user_form':user_form,
                                             'profile_form':profile_form,
                                             'announcements': Announcement.objects.all()},
                                             context_instance=RequestContext(request))

@login_required
def userUpdate(request):
    user_form = UserForm(request.POST, instance=request.user)
    profile_form = UserProfileForm(request.POST, instance=request.user.get_profile())
    
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return renderProfile(request, user_form, profile_form, 'Saved Successfully')
    return renderProfile(request, user_form, profile_form, 'Errors Exist')
