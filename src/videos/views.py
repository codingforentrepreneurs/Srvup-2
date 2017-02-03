import random
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
        CreateView,
        DetailView,
        ListView,
        UpdateView,
        DeleteView
    )

from .models import Video


class VideoCreateView(CreateView):
    queryset = Video.objects.all()

class VideoDetailView(DetailView):
    queryset = Video.objects.all() #.filter(title__icontains='vid')

    # def get_object(self):
    #     abc = self.kwargs.get("abc")
    #     print(abc)
    #     return get_object_or_404(Video, slug=abc)

    def get_context_data(self, *args, **kwargs):
        context = super(VideoDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


class VideoListView(ListView):
    queryset = Video.objects.all() #.filter(title__icontains='vid')

    # def get_queryset(self):
    #     return Video.objects.filter(title__icontains='vid') #.filter(user=self.request.user)


    def get_context_data(self, *args, **kwargs):
        context = super(VideoListView, self).get_context_data(*args, **kwargs)
        context['random_number'] = random.randint(100, 10000)
        print(context)
        return context


class VideoUpdateView(UpdateView):
    queryset = Video.objects.all()


class VideoDeleteView(DeleteView):
    queryset = Video.objects.all()




# Create

# Retreive

# Update

# Delete

# List

# Search