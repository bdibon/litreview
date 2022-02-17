from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import IntegerField, ModelForm
from django.forms.widgets import NumberInput

from .models import Review, Ticket, User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]
        help_texts = {
            "username": """
            Ce nom sera utilisé pour vous authentifier dans l'application,
            c'est celui sous lequel les autres utilisateurs vous verront.
            """
        }


class AuthenticationForm(AuthenticationForm):
    pass


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {"title": "Titre"}


class ReviewForm(ModelForm):
    rating = IntegerField(
        min_value=Review.MIN_RATING, max_value=Review.MAX_RATING
    )

    class Meta:
        model = Review
        fields = ["ticket", "headline", "rating", "body", "user"]
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}
