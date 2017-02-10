import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic import (
        CreateView,
        DetailView,
        ListView,
        UpdateView,
        DeleteView,
        RedirectView,
        View
    )

#from .forms import VideoForm
from analytics.models import CourseViewEvent


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



class LectureDetailView(View):
    def get(self, request, cslug=None, lslug=None, *args, **kwargs):
        obj = None
        qs = Course.objects.filter(slug=cslug).lectures().owned(request.user)
        if not qs.exists():
            raise Http404
        course_ = qs.first()
        if request.user.is_authenticated():
            view_event, created = CourseViewEvent.objects.get_or_create(user=request.user, course=course_)
            if view_event:
                view_event.views += 1
                view_event.save()

        lectures_qs = course_.lecture_set.filter(slug=lslug)
        if not lectures_qs.exists():
            raise Http404
        
        obj = lectures_qs.first()
        context = {
            "object": obj,
            "course": course_,
        }

        if not course_.is_owner and not obj.free: #and not user.is_member:
            return render(request, "courses/must_purchase.html", {"object": course_}) 

        return render(request, "courses/lecture_detail.html", context)



class CourseDetailView(DetailView):
    #queryset = Course.objects.all()
    def get_object(self):
        slug = self.kwargs.get("slug")
        qs = Course.objects.filter(slug=slug).lectures().owned(self.request.user)
        if qs.exists():
            obj = qs.first()
            if self.request.user.is_authenticated():
                view_event, created = CourseViewEvent.objects.get_or_create(user=self.request.user, course=obj)
                if view_event:
                    view_event.views += 1
                    view_event.save()
            return obj
        raise Http404


class CoursePurchaseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, slug=None):
        qs = Course.objects.filter(slug=slug).owned(self.request.user)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated():
                my_courses = user.mycourses
                # run transaction
                # if transaction successful:
                my_courses.courses.add(qs.first())
                return qs.first().get_absolute_url()
            return qs.first().get_absolute_url()
        return "/courses/"



class CourseListView(ListView):
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        print(dir(context.get('page_obj')))
        return context

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