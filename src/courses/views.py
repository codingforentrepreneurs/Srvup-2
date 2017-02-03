import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
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
from .models import Course


class CourseCreateView(StaffMemberRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(CourseCreateView, self).form_valid(form)




class CourseDetailView(MemberRequiredMixin, DetailView):
    queryset = Course.objects.all()


class CourseListView(ListView):
    def get_queryset(self):
        request = self.request
        qs = Course.objects.all()
        query = request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs  #.filter(title__icontains='vid') #.filter(user=self.request.user)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(VideoListView, self).get_context_data(*args, **kwargs)
    #     context['random_number'] = random.randint(100, 10000)
    #     print(context)
    #     return context


class CourseUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Course.objects.all()
    form_class = CourseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_staff:
            obj.user = self.request.user
        obj.save()
        return super(CourseUpdateView, self).form_valid(form)



class CourseDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Course.objects.all()
    success_url = '/videos/'