# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
import datetime


class Campaign(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return '%s (%s - %s)' % (self.title, self.start_date, self.end_date)

    @property
    def has_ended(self):
        return datetime.date.today() > self.end_date

    @classmethod
    def get_active(cls):
        today = datetime.date.today()
        return cls.objects.filter(start_date__lte=today, end_date__gte=today).first() # FIXME: add support for several campaigns simultaneously


class CampaignEntry(models.Model):
    campaign = models.ForeignKey('Campaign', related_name='entries', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='')
    created_at = models.DateTimeField()

