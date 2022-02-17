from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import ReviewForm, UserCreationForm, TicketForm
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


@login_required
def new_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.cleaned_data
            ticket["user"] = request.user
            Ticket(**ticket).save()
            # TODO: redirect to the posts page, where all the user's publicaiton belong.
            return redirect("core:home")
    else:
        form = TicketForm()

    return render(request, "litreviewcore/new_ticket.html", {"form": form})


@login_required
def new_review(request):
    ticket_id = request.GET.get("ticket")
    ticket = Ticket.objects.filter(pk=ticket_id).first()
    ticket_form = (
        TicketForm(request.POST, request.FILES)
        if request.method == "POST"
        else TicketForm()
    )

    if request.method == "POST":
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.cleaned_data

            if not ticket and ticket_form.is_valid():
                ticket = ticket_form.cleaned_data
                ticket["user"] = request.user
                ticket = Ticket(**ticket)
                ticket.save()

            review["ticket"] = ticket
            review["user"] = request.user
            Review(**review).save()
            return redirect("core:home")
    else:
        review_form = ReviewForm()

    user_is_author = (
        True if (not ticket or ticket.user == request.user) else False
    )

    return render(
        request,
        "litreviewcore/new_review.html",
        {
            "review_form": review_form,
            "ticket": ticket,
            "ticket_form": ticket_form,
            "user_is_author": user_is_author,
        },
    )


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
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
