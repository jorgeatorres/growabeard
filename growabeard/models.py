# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return '%s (%s - %s)' % (self.title, self.start_date, self.end_date)


class CampaignEntry(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='')
    created_at = models.DateTimeField()

