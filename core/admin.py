from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Job)
admin.site.register(models.Interview)
admin.site.register(models.Tracking)
