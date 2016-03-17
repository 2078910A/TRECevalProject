from django.contrib import admin
#<<<<<<< HEAD
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
#=======
from TREC.models import UserProfile

#admin.site.register(UserProfile)

# Register your models here.

#>>>>>>> 778b6a723403237c6fea7a84f08cb4051dd33fce
