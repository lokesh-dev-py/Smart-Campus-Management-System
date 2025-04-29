from django.urls import path
from student.views import dashboard
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    # Add more student-related URLs here
]