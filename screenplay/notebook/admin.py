from django.contrib import admin

# Register your models here.

from .models import ScreenPlay

class ScreenPlayAdmin(admin.ModelAdmin):
    list_display = ("case_no", "name", "filling_unit", "author", "path_url", "case_url")

admin.site.register(ScreenPlay, ScreenPlayAdmin)

