from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.models import User, Permission
from django.contrib.auth.admin import UserAdmin

from . import models


class ProfileInline(StackedInline):
    """Inline editor for the user profile."""

    model = models.Profile
    max_num = 1
    min_num = 1
    fk_name = "user"
    can_delete = False


class ProfileUserAdmin(UserAdmin):
    """The user admin with profile support."""

    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(models.User, ProfileUserAdmin)
admin.site.register(Permission)

admin.site.register(models.Story)
admin.site.register(models.Section)
admin.site.register(models.Image)
admin.site.register(models.Video)
admin.site.register(models.Audio)
admin.site.register(models.Comment)
