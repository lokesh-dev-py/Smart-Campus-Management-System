from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import RegistrationForm, PasswordResetForm
from users.utils import send_activation_email, send_password_reset_email
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from users.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Email confirmation pending
            user.save()

            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid64, 'token': token})
            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
            send_activation_email(user.email, activation_url)

            messages.success(
                request,
                "Registration successful! Please check your email to confirm your account."
            )
            return redirect('login')
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
            if user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
            else:
                messages.error(request, "User type not recognized.")
                return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    return render(request, 'users/login.html')


@csrf_protect
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user,
                                  data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            request.session.flush()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                uid64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid64, 'token': token})
                reset_url = f"{settings.SITE_DOMAIN}{reset_link}"
                send_password_reset_email(user.email, reset_url)
                messages.success(request, "Password reset link sent to your email.")
            else:
                messages.error(request, "Email not found.")
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            messages.error(request, ("This link is invalid or has expired."))
            return redirect('password_reset')
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            form = SetPasswordForm(user=user)
        return render(request, 'users/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "An error occurred. Please try again.")
        return redirect('password_reset')