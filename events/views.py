from django.shortcuts import render
from events.forms import EventForm
from events.models import Participant,Category
from django.http import HttpResponse

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def create_event(request):
    participants = Participant.objects.all()
    categories = Category.objects.all()
    form = EventForm(participants = participants, categories = categories)
    context = {"form": form}
    return render(request, "event_form.html", context)