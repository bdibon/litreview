from django.urls import path

from .views import (
    UserPostsView,
    home,
    new_review,
    signup,
    new_ticket,
    edit_ticket,
    delete_ticket,
    edit_review,
    delete_review,
)


app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path("tickets/new/", new_ticket, name="new-ticket"),
    path("tickets/<int:ticket_id>/edit/", edit_ticket, name="edit-ticket"),
    path(
        "tickets/<int:ticket_id>/delete/", delete_ticket, name="delete-ticket"
    ),
    path("reviews/new/", new_review, name="new-review"),
    path("reviews/<int:pk>/edit/", edit_review, name="edit-review"),
    path("review/<int:pk>/delete/", delete_review, name="delete-review"),
    path("user-posts/", UserPostsView.as_view(), name="user-posts"),
    path("accounts/signup/", signup, name="signup"),
]
