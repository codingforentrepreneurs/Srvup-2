from django.shortcuts import render
from django.views.generic import View

from categories.models import Category
from courses.models import Course, Lecture


class SearchView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET.get('q')) 
        return render(request, "search/default.html", {})