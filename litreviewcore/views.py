from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import generic
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.forms.models import model_to_dict

from .forms import ReviewForm, UserCreationForm, TicketForm
from .models import Review, Ticket, User, UserFollows


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
    tickets = (
        Ticket.objects.filter(user__in=following)
        .select_related("user")
        .prefetch_related("review_set")
    )

    # Concatenate the results.
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    # Paginate the results.
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "litreviewcore/home.html",
        {"posts": page_obj.object_list, "page_obj": page_obj},
    )


@method_decorator(login_required, name="dispatch")
class UserPostsView(generic.ListView):
    template_name = "litreviewcore/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        """Return the user's posts."""
        current_user = self.request.user

        reviews = Review.objects.filter(user=current_user).select_related(
            "ticket"
        )
        tickets = Ticket.objects.filter(user=current_user).prefetch_related(
            "review_set"
        )
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True,
        )

        return posts


@login_required
def new_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.cleaned_data
            ticket["user"] = request.user
            Ticket(**ticket).save()
            return redirect("core:user-posts")
    else:
        form = TicketForm()

    return render(request, "litreviewcore/new_ticket.html", {"form": form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket_new_data = form.cleaned_data
            ticket_new_data["user"] = request.user
            ticket.title = ticket_new_data.get("title")
            ticket.description = ticket_new_data.get("description")

            new_image = ticket_new_data.get("image")
            if new_image:
                ticket.image = new_image

            ticket.save()
            return redirect("core:user-posts")
    else:
        data = model_to_dict(ticket, fields=TicketForm.Meta.fields)
        form = TicketForm(data)

    return render(
        request,
        "litreviewcore/edit_ticket.html",
        {"ticket": ticket, "form": form},
    )


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        ticket.delete()
        return redirect("core:user-posts")

    return render(
        request, "litreviewcore/delete_ticket.html", {"ticket": ticket}
    )


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


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden()

    form = ReviewForm(
        request.POST or None,
        initial=model_to_dict(review),
    )
    if request.method == "POST" and form.is_valid():
        review.headline = form.cleaned_data["headline"]
        review.body = form.cleaned_data["body"]
        review.rating = form.cleaned_data["rating"]
        review.save()

        return redirect("core:user-posts")

    return render(
        request,
        "litreviewcore/edit_review.html",
        {"review": review, "form": form},
    )


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        review.delete()
        return redirect("core:user-posts")

    return render(
        request, "litreviewcore/delete_review.html", {"review": review}
    )


@login_required
def index_follows(request):
    user = request.user

    followings = UserFollows.objects.filter(user=user).select_related(
        "followed_user"
    )
    followers = UserFollows.objects.filter(followed_user=user).select_related(
        "user"
    )

    return render(
        request,
        "litreviewcore/user_follows.html",
        {"followings": followings, "followers": followers},
    )


@login_required
def subscribe(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    followed_user_username = request.POST.get("username")
    followed_user = get_object_or_404(User, username=followed_user_username)
    user_follows = UserFollows(user=request.user, followed_user=followed_user)
    user_follows.save()
    return redirect("core:user-follows")


@login_required
def unsubscribe(request, pk):
    user_follows = get_object_or_404(UserFollows, pk=pk)

    if user_follows.user == request.user:
        user_follows.delete()
    else:
        return HttpResponseForbidden()

    return redirect("core:user-follows")


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
