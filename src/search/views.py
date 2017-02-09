from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from categories.models import Category
from courses.models import Course, Lecture


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        qs = None
        c_qs = None
        l_qs = None
        if query:
            lec_lookup =  Q(title__icontains=query)\
             | Q(description__icontains=query)
            # lookup2 =  Q(title__icontains=query) & Q(description__icontains=query)
            query_lookup = lec_lookup | Q(category__title__icontains=query)\
             | Q(category__description__icontains=query)\
             | Q(lecture__title__icontains=query)\
            
            qs = Course.objects.all().lectures().filter(
                        query_lookup
                    ).distinct()
            
            qs_ids = [x.id for x in qs]

            cat_lookup = Q(primary_category__in=qs_ids) | Q(secondary_category__in=qs_ids)
            c_qs = Category.objects.filter(lec_lookup | cat_lookup).distinct()
            l_qs = Lecture.objects.filter(lec_lookup).distinct()

        context = {"qs": qs, "c_qs": c_qs, "l_qs": l_qs}
        return render(request, "search/default.html", context)




