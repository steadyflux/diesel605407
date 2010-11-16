from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from diesel.fuel.models import AnnouncementForm, Announcement

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