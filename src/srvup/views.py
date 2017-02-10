import random
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from analytics.models import CourseViewEvent
from courses.models import Course

def home(request):
    print(request)
    print(request.user)
    print(request.path)
    #return HttpResponse("Hello")
    return render(request, "home.html", {})


class HomeView(View):
    def get(self, request, *args, **kwargs): # GET -- retrieve view / list view / search
        course_qs = Course.objects.all().lectures().owned(request.user)
        qs = course_qs.featured().distinct().order_by("?")[:6]
        event_qs = CourseViewEvent.objects.all().prefetch_related("course")
        if request.user.is_authenticated():
            event_views = event_qs.filter(user=request.user)
        else:
            event_views = event_qs.filter(views__gte=10)
        
        event_views = event_views.order_by('views')[:20]
        ids_ = [x.course.id for x in event_views]
        print(ids_)
        rec_courses = course_qs.filter(id__in=ids_).order_by('?')[:6]
        context = {
            "qs": qs,
            "rec_courses": rec_courses,
            "name": "Justin",
            "random_number": random.randint(500, 1000)
        }
        return render(request, "home.html", context)

    # def post(self, request, *args, **kwargs): # POST -- create view
    #     return HttpResponse("Hello")

    # def put(self, request, *args, **kwargs): # PUT -- update view
    #     return HttpResponse("Hello")

    # def delete(self, request, *args, **kwargs): # DELETE -- delete view
    #     return HttpResponse("Hello")