from django.urls import path
from teacher.views import dashboard
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    # Add more teacher-related URLs here
]