from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F

from .forms import UserCreationForm
from .models import Review, Ticket, User


@login_required
def home(request):
    user = request.user

    # Get all the users that THE USER follows.
    following = User.objects.filter(
        Q(followed_by__user=user) | Q(pk__exact=user.id)
    )

    # Get their reviews and tickets.
    reviews = Review.objects.filter(user__in=following).select_related(
        "user", "ticket"
    )
    tickets = Ticket.objects.filter(user__in=following).select_related("user")

    # Concatenate the results.
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, "litreviewcore/home.html", {"posts": posts})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("core:home")
        else:
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})
