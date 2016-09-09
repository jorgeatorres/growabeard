"""growabeard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from . import views, settings

urlpatterns = [
    url(r'^c/(?P<id>[0-9]+)/$', views.campaign_details, name='campaign-details'),
    url(r'^upload/$', views.upload, name='upload'),

    url(r'^$', views.index, name='index'),
    url(r'^beard/(?P<id>[0-9]+)/$', views.beard_details, name='beard-details'),
    url(r'^beard/(?P<id>[0-9]+)/rotate/$', views.beard_rotate, name='beard-rotate'),

    #url(r'^', include('django.contrib.auth.urls')),
    url(r'^login/$', views.twitter_login, name='login'),
    url(r'^authenticated/$', views.twitter_authenticate, name='authenticated'),

    url(r'^admin/', admin.site.urls),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
