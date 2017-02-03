"""srvup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from .views import home, HomeView
from videos.views import (
    VideoListView, 
    VideoDetailView, 
    VideoCreateView, 
    VideoUpdateView,
    VideoDeleteView
    )

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^videos/$', VideoListView.as_view(), name='video-list'),
    url(r'^videos/create/$', VideoCreateView.as_view(), name='video-create'),
    # url(r'^videos/(?P<pk>\d+)/$', VideoDetailView.as_view(), name='video-detail'),
    url(r'^videos/(?P<slug>[\w-]+)/$', VideoDetailView.as_view(), name='video-detail-slug'),
    url(r'^videos/(?P<slug>[\w-]+)/edit/$', VideoUpdateView.as_view(), name='video-update'),
    url(r'^videos/(?P<slug>[\w-]+)/delete/$', VideoDeleteView.as_view(), name='video-delete'),

]
