# encoding: utf-8
from django.contrib import admin
from .models import User, Campaign, CampaignEntry

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    fields = (('start_date', 'end_date'), 'title')

@admin.register(CampaignEntry)
class CampaignEntryAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'file', 'created_at')
    fields = ('campaign', 'user', 'file', 'created_at')
