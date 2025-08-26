from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from .models import AttendanceEvent, Student, Class
from .resource import AttendanceEventResource, StudentResource

admin.site.register(Class)

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_classes = [StudentResource]


@admin.register(AttendanceEvent)
class AttendanceEventAdmin(ImportExportModelAdmin):
    resource_classes = [AttendanceEventResource]