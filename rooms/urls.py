from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.RoomsView.as_view()),
    path("<int:pk>/", views.RoomsView.as_view()),
]
