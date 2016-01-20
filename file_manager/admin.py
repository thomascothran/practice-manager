from django.contrib import admin
from .models import FileObj, FileManagerTags, Note

# Register your models here.

admin.site.register(FileObj)
admin.site.register(FileManagerTags)
admin.site.register(Note)