from django.urls import include, path
from polls.views import *
urlpatterns = [
    path('', Homepage.as_view(), name = "main"),
    path("__reload__/", include("django_browser_reload.urls")),
]