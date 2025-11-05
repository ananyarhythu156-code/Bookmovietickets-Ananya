from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from. import models
admin.site.register(models.Movies)
admin.site.register(models.Category)
admin.site.register(models.Genre)
admin.site.register(models.Theater)
admin.site.register(models.Showtime)
admin.site.register(models.Feedback)
admin.site.register(models.Director)
admin.site.register(models.Producer)
admin.site.register(models.Actor)
admin.site.register(models.Actress)