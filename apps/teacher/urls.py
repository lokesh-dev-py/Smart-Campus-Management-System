from django.urls import path
from teacher.views import dashboard
urlpatterns = [
    path('teacher-dashboard/', dashboard, name='teacher_dashboard'),
    # Add more teacher-related URLs here
]