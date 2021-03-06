from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from diesel.fuel.models import AnnouncementForm, Announcement, UserProfileForm,\
    UserProfile, UserForm, Station, FuelPrice, StationUserComments,\
    StationUserCommentsForm
from diesel.fuel.stationtools import searchQuery
from diesel.fuel.forms import SearchForm, UploadFileForm, PriceForm
from django.http import HttpResponseRedirect

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

@login_required
def userDelete(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("/fuel/")


def searchScreen(request):    
    searchFields = SearchForm(initial={'centane_rating': 'Unknown'})
    return render_to_response('search.html', {
                                              'search_form': searchFields,
                                              'announcements': Announcement.objects.all()},
                                             context_instance=RequestContext(request))

def searchPerform(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_form = form.cleaned_data
            location = ""
            if search_form['address']:
                location += search_form['address'] + ","
            if search_form['city']:
                location += search_form['city'] + ","
            if search_form['state']:
                location += search_form['state'] + ","
            if search_form['zip']:
                location += search_form['zip']
            location = location.rstrip().rstrip(',')
            print location
            centane_filter = None
            if search_form['centane_rating']:
                centane_filter = search_form['centane_rating']
            print centane_filter
            results = searchQuery(location, search_form['num_results'], centane_filter)
    return render_to_response('search.html', {
                                              'search_form': form,
                                              'announcements': Announcement.objects.all(),
                                              'results': results},
                                             context_instance=RequestContext(request))
    

def stationHome(request, id):
    print id
    station = Station.objects.get(id=id)
    return render_to_response('station.html', {
                                              'station': station,
                                              'announcements': Announcement.objects.all(),
                                              'image_upload_form': UploadFileForm(),
                                              'price_form': PriceForm(),
                                              'comments': StationUserComments.objects.filter(station=id),
                                              'comment_form': StationUserCommentsForm()},
                                             context_instance=RequestContext(request))
    


@login_required
def uploadStationImage(request, id):
    if request.method == 'POST':
        station = Station.objects.get(id=id)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            station.image = request.FILES['file']
            station.save()
        else:
            print form.errors
    else:
        form = UploadFileForm()
    return HttpResponseRedirect('/fuel/station/' + id)

@login_required
def priceUpdate(request, id):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            new_price = FuelPrice.objects.create(station_id = id, price = request.POST['price'])
            new_price.save()
        else:
            print form.errors
    return HttpResponseRedirect('/fuel/station/' + id)

@login_required
def addStationComment(request, id):
    if request.method == 'POST':
        form = StationUserCommentsForm(request.POST)
        if form.is_valid():
            new_comment = StationUserComments.objects.create(station_id = id, text=request.POST['text'], user=request.user)
            new_comment.save()
        else:
            print form.errors
    return HttpResponseRedirect('/fuel/station/' + id)
