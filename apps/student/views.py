from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'student/student_dashboard.html')




