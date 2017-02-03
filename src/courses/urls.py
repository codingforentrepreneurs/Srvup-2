from django.conf.urls import url


from .views import (
    CourseListView, 
    CourseDetailView, 
    #CourseCreateView, 
    #CourseUpdateView,
    CourseDeleteView
    )

urlpatterns = [
    url(r'^$', CourseListView.as_view(), name='list'),
    #url(r'^videos/create/$', VideoCreateView.as_view(), name='video-create'),
    url(r'^(?P<slug>[\w-]+)/$', CourseDetailView.as_view(), name='detail'),
    #url(r'^videos/(?P<slug>[\w-]+)/edit/$', VideoUpdateView.as_view(), name='video-update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', CourseDeleteView.as_view(), name='delete'),
]

