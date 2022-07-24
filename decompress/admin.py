from django.contrib import admin
from .models import TestFile
from django.conf import settings


admin.site.register(TestFile)

admin.site.site_header = f"{settings.SITE_NAME} Portal"
admin.site.site_title = f"{settings.SITE_NAME} Admin"
admin.site.index_title = f"{settings.SITE_NAME} Dashboard"
