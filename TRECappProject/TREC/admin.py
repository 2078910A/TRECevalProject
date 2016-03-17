from django.contrib import admin
from TREC.models import *


class TrackAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
        }


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
        }

admin.site.register(UserProfile)
admin.site.register(Track, TrackAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Run)
