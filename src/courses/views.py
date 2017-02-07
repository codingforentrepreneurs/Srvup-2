import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import (
        CreateView,
        DetailView,
        ListView,
        UpdateView,
        DeleteView
    )

#from .forms import VideoForm
from videos.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from .forms import CourseForm
from .models import Course, Lecture, MyCourses


class CourseCreateView(StaffMemberRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(CourseCreateView, self).form_valid(form)



class LectureDetailView(MemberRequiredMixin, DetailView):
    def get_object(self):
        course_slug = self.kwargs.get("cslug")
        lecture_slug = self.kwargs.get('lslug')
        obj = get_object_or_404(Lecture, course__slug=course_slug, slug=lecture_slug)
        return obj


class CourseDetailView(MemberRequiredMixin, DetailView):
    #queryset = Course.objects.all()
    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Course.objects.filter(slug=slug).owned(self.request.user)
        if obj.exists():
            return obj.first()
        raise Http404


class CourseListView(ListView):
    def get_queryset(self):
        request = self.request
        qs = Course.objects.all()
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(title__icontains=query)
        if user.is_authenticated():
            qs = qs.owned(user)
        return qs 


class CourseUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Course.objects.all()
    form_class = CourseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_staff:
            obj.user = self.request.user
        obj.save()
        return super(CourseUpdateView, self).form_valid(form)

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404



class CourseDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Course.objects.all()
    success_url = '/videos/'

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404