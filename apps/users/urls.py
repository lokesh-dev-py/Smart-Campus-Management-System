from django.urls import path
from users.views import home, register_view, login_view, activate_account
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
]