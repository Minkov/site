import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from jose import jws

import json
import requests

from judge.models import Profile, Language


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    return render(request, 'oidc/login.html')

@csrf_protect
def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    auth.logout(request)
    return render(request, 'oidc/logout.html')


def signin_oidc(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    return render(request, 'oidc/signin-oidc.html')


@csrf_protect
def token(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    print(' --- /token ---', datetime.datetime.now())

    # keys_raw = requests.get(
    #     'https://login.microsoftonline.com/tfp/telerikacademyidentity.onmicrosoft.com/B2C_1A_signup_signin/discovery/keys').text
    keys_raw = requests.get(
        'https://login.microsoftonline.com/tfp/telerikacademyauth.onmicrosoft.com/B2C_1A_signup_signin/discovery/keys').text
    keys = json.loads(keys_raw)
    print('1')
    access_token = request.POST['access_token']
    print('2')
    claims = json.loads(jws.verify(access_token, keys, algorithms=['RS256']))
    print('3')

    email = claims['emails']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        username = ''.join(ch for ch in email if ch.isalnum() or ch == '_')
        user = User(username=username, email=email)
        user.save()

    profile, _ = Profile.objects.get_or_create(user=user, defaults={
        'language': Language.get_python2(),
        'timezone': 'Europe/Sofia',
    })

    profile.name = email[:email.index('@')]

    profile.save()

    # if result['IsAdmin']:
    #     user.is_staff = True
    #     user.is_superuser = True
    # else:
    #     user.is_staff = False
    #     user.is_superuser = False
    # user.save()
    auth.login(request, user, 'django.contrib.auth.backends.ModelBackend')

    return HttpResponseRedirect('/')
