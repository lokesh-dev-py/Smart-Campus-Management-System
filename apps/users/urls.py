from django.urls import path
from users.views import home, register_view, login_view, activate_account, password_change_view, password_reset_view, password_reset_confirm
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', password_change_view, name='change_password'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),

]