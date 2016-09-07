# encoding: utf-8
from datetime import date, datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign, User
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
    total_days = (campaign.end_date - campaign.start_date).days

    beards = _members_and_their_beards(campaign, True)

    return render(request, 'campaign.html', dict(campaign=campaign, total_days=total_days, beards=beards))


def _members_and_their_beards(campaign, include_future=False):
    today = date.today()

    if campaign.end_date >= today and not include_future:
        total_days = (today - campaign.start_date).days + 1
    else:
        total_days = (campaign.end_date - campaign.start_date).days + 1

    days = [campaign.start_date + timedelta(days=i) for i in range(0, total_days)]
    members = [User.objects.get(pk=x) for x in campaign.entries.values_list('user__id', flat=True).distinct()]

    res = dict()

    for m in members:
        res[m] = []

        for d in days:
            e = campaign.entries.filter(user=m, created_at__date=d).first()
            res[m].append({'day': d, 'item': e})

    return res
