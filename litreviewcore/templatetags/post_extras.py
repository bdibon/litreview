from django import template

from ..models import Review


register = template.Library()


@register.filter
def is_review(post):
    return isinstance(post, Review)


@register.inclusion_tag("litreviewcore/rating.html")
def get_stars(rating):
    stars = range(Review.MIN_RATING + 1, Review.MAX_RATING + 1)
    return {"stars": stars, "rating": rating}


@register.inclusion_tag("litreviewcore/review.html")
def show_review(review, user, is_user_posts=False, is_delete_post=False):
    user_is_author = False
    if review.user == user:
        user_is_author = True
    return {
        "review": review,
        "user_is_author": user_is_author,
        "user": user,
        "is_user_posts": is_user_posts,
        "is_delete_post": is_delete_post,
    }


@register.inclusion_tag("litreviewcore/ticket.html")
def show_ticket(ticket, user, is_user_posts=False, is_delete_post=False):
    user_is_author = False
    if ticket.user == user:
        user_is_author = True
    return {
        "ticket": ticket,
        "user_is_author": user_is_author,
        "is_user_posts": is_user_posts,
        "is_delete_post": is_delete_post,
    }
