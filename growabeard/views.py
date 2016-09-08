# encoding: utf-8
import oauth2 as oauth
import cgi
from datetime import date, datetime, timedelta
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse

import settings
from .models import Campaign, CampaignEntry, User, Profile
from .forms import UploadForm


def index(request):
    campaign = Campaign.get_active()

    if not campaign:
        return render(request, 'no-campaign.html')

    return redirect('campaign-details', campaign.id)


@login_required
def upload(request):
    campaign = Campaign.get_active()

    if not campaign:
        return HttpResponseForbidden()

    today = date.today()

    if campaign.entries.filter(user=request.user, created_at__date=today).exists():
        messages.error(request, 'You\'ve already uploaded an image for today.')
        return redirect('/')

    form = UploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        campaign.entries.create(user=request.user, file=request.FILES['image'], created_at=datetime.now())
        messages.success(request, 'Thanks for sharing your beard progress!')
        return redirect('/')

    return render(request, 'upload.html', dict(form=form))


def campaign_details(request, id):
    campaign = get_object_or_404(Campaign, pk=id)
    beards = campaign.get_beards()
    return render(request, 'campaign.html', dict(campaign=campaign, beards=beards))


def twitter_login(request, action=''):
    consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    client = oauth.Client(consumer)
    response, content = client.request('https://api.twitter.com/oauth/request_token', "GET")

    if response['status'] != '200':
        print content
        raise Exception("Invalid response from Twitter.")

    request.session['next'] = request.GET.get('next', None)
    request.session['request_token'] = dict(cgi.parse_qsl(content))

    url = "{0}?oauth_token={1}".format(
        'https://api.twitter.com/oauth/authenticate',
        request.session['request_token']['oauth_token']
    )

    return HttpResponseRedirect(url)


def twitter_authenticate(request):
    token = oauth.Token(
        request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret']
    )
    token.set_verifier(request.GET['oauth_verifier'])

    consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    client = oauth.Client(consumer, token)
    response, content = client.request('https://api.twitter.com/oauth/access_token', "GET")

    if response['status'] != '200':
        print content
        raise Exception("Invalid response from Twitter.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797',
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content))

    print access_token

    try:
        user = User.objects.get(username=access_token['screen_name'])
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=access_token['screen_name'],
            email='%s@twitter.com' % access_token['screen_name'],
            password=access_token['oauth_token_secret']
        )

        profile = Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    user = authenticate(
        username=access_token['screen_name'],
        password=access_token['oauth_token_secret']
    )

    if user:
        print user
        print user.is_anonymous()
        print user.is_authenticated()
    else:
        print "No user!"

    login(request, user)

    if 'next' in request.session and request.session['next']:
        redirect_url = request.session['next']
    else:
        redirect_url = settings.LOGIN_REDIRECT_URL

    return HttpResponseRedirect(redirect_url)


def beard_details(request, id):
    entry = get_object_or_404(CampaignEntry, pk=id)

    if not request.is_ajax():
        u = reverse('campaign-details', args=[entry.campaign.id,]) + u'#beard-%d' % entry.id
        return redirect(u)

    return render(request, 'beard-details.html', {'entry': entry})


def beard_rotate(request, id):
    entry = get_object_or_404(CampaignEntry, pk=id)

    if not entry.user == request.user:
        return HttpResponseForbidden()

    entry.rotate()
    messages.success(request, 'Image rotated!')
    u = reverse('campaign-details', args=[entry.campaign.id,]) + u'#beard-%d' % entry.id
    return redirect(u)

