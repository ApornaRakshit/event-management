from django.shortcuts import render
from django.http import HttpResponse
from events.forms import EventModelForm
from events.models import Participant, Category

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def create_event(request):
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, "event_form.html", {"form": form, "message": "Event added successfully"})

    context = {"form": form}
    return render(request, "event_form.html", context)