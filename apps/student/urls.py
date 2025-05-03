from django.urls import path
from student.views import dashboard
urlpatterns = [
    path('stu-dashboard/', dashboard, name='student_dashboard'),
    # Add more student-related URLs here
]