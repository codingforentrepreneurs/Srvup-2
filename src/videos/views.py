from django.shortcuts import render
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
    queryset = Video.objects.all()


class VideoListView(ListView):
    queryset = Video.objects.all()


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