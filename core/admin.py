from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Story)
admin.site.register(models.Category)
admin.site.register(models.Image)

admin.site.register(models.Profile)