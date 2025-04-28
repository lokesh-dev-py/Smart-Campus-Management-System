from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import RegistrationForm

# Create your views here.
def register_view(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False  # Set to False until email confirmation
        user.save()
        # HERE SHOULD BE THE EMAIL CONFIRMATION LOGIC
        messages.success(
            request, 
            "Registration successful! Please check your email to confirm your account."
        )
        return redirect('login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    return render(request, 'users/login.html')