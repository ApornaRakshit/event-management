
from django.shortcuts import render

def home(request):
    is_organizer = False
    if request.user.is_authenticated:
        is_organizer = request.user.groups.filter(name='Organizer').exists()
    return render(request, 'home.html', {'is_organizer': is_organizer})


def no_permission(request):
    return render(request, 'no_permission.html')
