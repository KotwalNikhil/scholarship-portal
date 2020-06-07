from django.contrib import admin
from .models import student,staff,profile
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(student)
admin.site.register(staff)
#admin.site.register(profile)

@admin.register(profile)
class profileAdmin(ImportExportModelAdmin):
    pass