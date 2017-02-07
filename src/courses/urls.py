from django.conf.urls import url


from .views import (
    CourseListView, 
    CourseDetailView, 
    CourseCreateView, 
    CourseUpdateView,
    CourseDeleteView,
    LectureDetailView,
    CoursePurchaseView
    )

urlpatterns = [
    url(r'^$', CourseListView.as_view(), name='list'),
    url(r'^create/$', CourseCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/purchase/$', CoursePurchaseView.as_view(), name='purchase'),
    url(r'^(?P<cslug>[\w-]+)/(?P<lslug>[\w-]+)/$', LectureDetailView.as_view(), name='lecture-detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', CourseUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', CourseDeleteView.as_view(), name='delete'),
]

