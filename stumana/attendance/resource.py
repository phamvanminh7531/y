from import_export import resources
from .models import AttendanceEvent, Student, Class
from import_export import fields
from import_export.widgets import ForeignKeyWidget

class AttendanceEventResource(resources.ModelResource):
    student = fields.Field(
        column_name = 'student',
        attribute = 'student',
        widget=ForeignKeyWidget(Student, field='code')
    )
    class Meta:
        model = AttendanceEvent
        fields = ('student', 'date', 'duration')

class StudentResource(resources.ModelResource):
    class_name = fields.Field(
        column_name = 'class_name',
        attribute = 'class_name',
        widget=ForeignKeyWidget(Class, field='class_name')
    )
    class Meta:
        model = Student
        exclude = ('id',)
        fields = ('code', 'class_name')
        import_id_fields = ('code',)