# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.ForeignKey(User)
    twitter_token = models.CharField(max_length=255)
    twitter_secret = models.CharField(max_length=255)


class Campaign(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return '%s (%s - %s)' % (self.title, self.start_date, self.end_date)

    @property
    def has_ended(self):
        return datetime.date.today() > self.end_date

    def get_beards(self):
        return BeardsHelper(campaign=self)

    @classmethod
    def get_active(cls):
        today = datetime.date.today()
        return cls.objects.filter(start_date__lte=today, end_date__gte=today).first() # FIXME: add support for several campaigns simultaneously


class CampaignEntry(models.Model):
    campaign = models.ForeignKey('Campaign', related_name='entries', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='')
    created_at = models.DateTimeField()

    def rotate(self):
        import StringIO
        from django.core.files.base import ContentFile
        from PIL import Image
        import os.path

        orig = StringIO.StringIO(self.file.read())
        rotated = StringIO.StringIO()

        image = Image.open(orig)
        #image = image.rotate(-90, expand=True)
	image = image.transpose(Image.ROTATE_90)
        image.save(rotated, 'PNG')

        self.file.save(os.path.basename(self.file.path), ContentFile(rotated.getvalue()))


class BeardsHelper(object):

    def __init__(self, campaign):
        self.campaign = campaign
        self.today = datetime.date.today()
        self.total_days = (campaign.end_date - campaign.start_date).days + 1
        self.days = [campaign.start_date + datetime.timedelta(days=i) for i in range(0, self.total_days)]
        self.members = [User.objects.get(pk=x) for x in campaign.entries.values_list('user__id', flat=True).distinct()]

    @property
    def entries(self):
        res = {}


        for m in self.members:
            res[m] = []

            for d in self.days:
                entry = self.campaign.entries.filter(user=m, created_at__date=d).first()
                res[m].append({'date': d, 'entry': entry, 'today': ( d == self.today ), 'past': ( d < self.today ), 'future': ( d > self.today ) })

        return res

