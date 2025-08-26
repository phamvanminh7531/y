from django.db import models



# Create your models here.
class Class(models.Model):
    class_name = models.CharField(max_length=6, unique=True, blank=False, null=False)

    def __str__(self):
        return self.class_name

class Student(models.Model):
    code = models.CharField(max_length=8, unique=True, blank=False, null=False)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.code

class AttendanceEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.FloatField()

    def __str__(self):
        return self.student.code