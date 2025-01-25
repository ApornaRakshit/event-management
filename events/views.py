from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Event management system")

def contact(request):
    return HttpResponse("<h1>This is contact</h1>")

def show_event(reqruest):
    return HttpResponse("This is our task page")