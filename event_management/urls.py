from django.contrib import admin
from django.urls import path, include
from events.views import home, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home),
    path("contact/", contact),
    path("events/", include("events.urls"))
]
