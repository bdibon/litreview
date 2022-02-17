from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="book_covers/")
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    MAX_RATING = 5
    MIN_RATING = 0

    ticket = models.ForeignKey(Ticket, blank=True, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING),
        ]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="utilisateur",
    )
    followed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followed_by",
        verbose_name="utilisateur suivi",
    )

    class Meta:
        verbose_name_plural = "utilisateur suit"
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        constraints = [
            models.UniqueConstraint(
                "user", "followed_user", name="unique_user_followed_user"
            ),
            models.CheckConstraint(
                check=~models.Q(user__exact=models.F("followed_user")),
                name="user_not_followed_user",
            ),
        ]
