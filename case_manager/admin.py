from django.contrib import admin
from .models import Case, CaseType
from tasks.models import Task, Project

# Register your models here.

# Admin view for Cases
class CaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info',      {'fields': ['type_of_case',
                                        'client',
                                        'related_parties',
                                        'description_of_case',
                                        'retainer_agreement']}),
        ('Related Tasks',   {'fields': ['related_tasks',
                                        'related_projects'],
                             'classes': ['collapse']}),
        ('Billing',         {'fields':['hourly',
                                       'attorney_hourly_rate',
                                       'assistant_hourly_rate'],
                             'classes': ['collapse']})

    )

admin.site.register(Case, CaseAdmin)


# Admin view for CaseTypes
admin.site.register(CaseType)