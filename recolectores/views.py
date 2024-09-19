from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import OrderForm
# Create your views here.

def nueva_orden(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = OrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/index/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderForm()

    return render(request, "nueva_orden.html", {"form": form})

def index(request):
    return render(request, "index.html")
