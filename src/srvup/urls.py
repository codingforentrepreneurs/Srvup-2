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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
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
    # url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^videos/', include('videos.urls', namespace='videos')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





