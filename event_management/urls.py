from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home
# from events.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('events', include('events.urls')),
    path('', include('events.urls')),
    path('', include('core.urls')),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    # path('',home, name="home")
] + debug_toolbar_urls()