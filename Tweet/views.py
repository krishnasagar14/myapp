from django.shortcuts import render

# Create your views here.

from code.T2 import Tweet_Code as TC
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models

C = TC()

def main(request):
    return render(request, 'login.html')

def twitter_login(request):
    url = C.TLogin()
    return HttpResponseRedirect(url)

@login_required(login_url='/Tweet/main/')
def twitter_logout(request):
    logout(request)
    return HttpResponseRedirect('/Tweet')

def twitter_authenticated(request):
    access_token = C.TAuthenticate(request=request)
    
    try:
        user = User.objects.get(username=access_token['screen_name'])
    except User.DoesNotExist:
        user = User.objects.create_user(access_token['screen_name'], '%s@twitter.com' % access_token['screen_name'], access_token['oauth_token_secret'])

        profile = models.Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()
    
    user = authenticate(username=access_token['screen_name'], password=access_token['oauth_token_secret'])
    request.session['screen_name'] = access_token['screen_name']
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/Tweet/home')
        else:
            return render(request,'error.html', {'error':'User not authenticated. User account may not be present'})
    else:
        return render(request,'error.html', {'error':'User not authenticated. Username or passwork is invalid'})

@login_required(login_url='/Tweet/login/')
def home_page(request):
    if hasattr(C, 'access_token'):
        data = C.access_token['screen_name']
        content = C.THome()
        return render(request,'main.html',{'data':data, 'content':content})
    else:
        return HttpResponseRedirect('/Tweet')

def internal(request):
    if request.method == 'GET':
        if request.GET['page'] == 'page1':
            C.TTweet(s=request.GET['message'])
    return HttpResponse("SuccessFully Saved")
