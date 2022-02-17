from django.urls import path

from .views import home, new_review, signup, new_ticket


app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path("tickets/new/", new_ticket, name="new-ticket"),
    path("review/new/", new_review, name="new-review"),
    path("accounts/signup", signup, name="signup"),
]
