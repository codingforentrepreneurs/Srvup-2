from django.shortcuts import render
from django.views.generic import (
        CreateView,
        DetailView,
        ListView,
        UpdateView,
        DeleteView,
        RedirectView
    )

from .models import Category


class CategoryListView(ListView):
    queryset = Category.objects.all()


class CategoryDetailView(DetailView):
    queryset = Category.objects.all()