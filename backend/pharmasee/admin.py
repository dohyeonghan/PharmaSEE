from django.contrib import admin
from .models import Pill, Reminder
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Pill)
class PillAdmin(admin.ModelAdmin):
    list_display = ['image_dir_tag','name','effect','side_effect']
    list_display_links = ['name']

    def image_dir_tag(self, pill):
        return mark_safe(f"<img src={pill.image_dir.url} style='width: 100px;' />")


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'dose', 'when_to_take','taken_time', 'is_taken_today']
    pass