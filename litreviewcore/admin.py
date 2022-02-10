from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Ticket, Review, UserFollows

# admin.site.register(User, UserAdmin)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)


class UserFollowsAnotherUserInline(admin.StackedInline):
    model = UserFollows
    extra = 1
    fk_name = "user"
    verbose_name = "l'utilisateur suit"
    verbose_name_plural = "utilisateurs suivis"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserFollowsAnotherUserInline]
