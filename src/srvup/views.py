from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


def home(request):
    print(request)
    print(request.user)
    print(request.path)
    #return HttpResponse("Hello")
    return render(request, "home.html", {})


class HomeView(View):
    def get(self, request, *args, **kwargs): # GET -- retrieve view / list view / search
        return HttpResponse("Hello")

    def post(self, request, *args, **kwargs): # POST -- create view
        return HttpResponse("Hello")

    def put(self, request, *args, **kwargs): # PUT -- update view
        return HttpResponse("Hello")

    def delete(self, request, *args, **kwargs): # DELETE -- delete view
        return HttpResponse("Hello")