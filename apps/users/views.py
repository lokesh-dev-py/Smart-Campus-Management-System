from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import RegistrationForm
from users.utils import send_activation_email
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from users.models import User
from django.contrib.auth import authenticate, login
# Create your views here.
def register_view(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False  # Set to False until email confirmation
        user.save()
        # HERE SHOULD BE THE EMAIL CONFIRMATION LOGIC
        uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_link = reverse('activate', kwargs={'uidb64': uid64, 'token': token})
        activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
        # Send email with activation_url
        send_activation_email(user.email, activation_url)
        messages.success(
            request, 
            "Registration successful! Please check your email to confirm your account."
        )
        return redirect('login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(request, "Account already activated.")
            return redirect('login')
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired.")
            return redirect('register')
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('register')
    
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        elif request.user.is_student:
            return redirect('student_dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('login')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        if not user.is_active:
            messages.error(request, "Account is not activated. Please check your email.")
            return redirect('login')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            if user
    return render(request, 'users/login.html')