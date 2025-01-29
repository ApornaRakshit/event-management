from django.urls import path
from events.views import manager_dashboard, user_dashboard,create_event

urlpatterns = [
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard),
    # path('test/',test),
    path('create-event/',create_event)
]
