from django.urls import path
from .views import home, student_list

urlpatterns = [
    path("", home),
    path("student/", student_list, name="student_list"),
]
