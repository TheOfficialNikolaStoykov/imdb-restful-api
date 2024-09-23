from django.contrib import admin

from media_app import models

admin.site.register(models.StreamingPlatform)
admin.site.register(models.Media)
admin.site.register(models.Review)