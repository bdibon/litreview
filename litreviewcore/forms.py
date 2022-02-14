from django.contrib.auth.forms import UserCreationForm

from .models import User


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
