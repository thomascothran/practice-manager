from django.contrib import admin
from .models import Project, Task, Context

# CLASSES

class TaskAdmin(admin.ModelAdmin):

    """
    This controls how your projects show up in the administrative
    interface
    """
    fieldsets = [
        (None,          {'fields': ['name', 'notes']}),
        ('Tags',        {'fields': ['status']}),
        ('Reminders',   {'fields' : ['due_date'],
                         'classes' : ['collapse']}),
        ('Related Projects', {'fields': ['related_project'],
                              'classes': ['collapse']})
    ]

    list_display = ['name', 'status', 'due_date']
    """
    Controls what shows up in the admin user interface table
    """

    list_filter = ['due_date', 'status']

    search_fields = ['name', 'notes']


class ProjectAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,          {'fields': ['name']}),
        ('Details',     {'fields': ['purpose', 'vision', 'big_steps']}),
        ('Tags',        {'fields': ['status']}),
        ('Dates',       {'fields': ['due_date'], 'classes': ['collapse']}),
        ('Related Projects', {'fields': ['related_project']}),
    ]

    list_display = ['name', 'status', 'due_date']

    list_filter = ['due_date', 'status']

    search_fields = ['name', 'purpose', 'vision', 'big_steps']

class ContextAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',     {'fields': ['name', 'description']}),
        ('Related',     {'fields': ['user']}),
    ]

    list_display = ['name', 'description', 'user']

    list_filter = ['name', 'description', 'user']

    search_fields = ['name', 'description', 'user']


# Register your models here.

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Context, ContextAdmin)