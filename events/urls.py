from django.urls import path
from events.views import create_event,organizer_dashboard, update_event

urlpatterns = [
    # path('manager-dashboard/', manager_dashboard),
    # path('user-dashboard/', user_dashboard),
    path('organizer-dashboard/', organizer_dashboard, name="organizer-dashboard"),
    path('create-event/',create_event),
    path('update-event/<int:id>/', update_event, name="update-event")
    # path('view_event/', view_event)
]
