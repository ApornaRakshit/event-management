from django.shortcuts import render
from django.http import HttpResponse
from events.forms import EventForm,EventModelForm
from events.models import Employee,Event

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    names=["Mahmud", "Aps","Mars","Bushri"]
    count=0
    for name in names:
        count += 1
    context = {
        "name" : names,
        "age" : 23,
        "count" : count
    }
    return render(request, 'test.html',context)

def create_event(request):
    # employees = Employee.objects.all()
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'event_form.html',{"form":form, "message": "Event added successfully"})

            """ For Model form data """
            ''' For django data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # event = Event.objects.create(
            #     title=title, description=description,due_date=due_date)
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     event.assigned_to.add(employee)

            # return HttpResponse("Event Added successfully")

    context = {"form": form}
    return render(request,"event_form.html", context)