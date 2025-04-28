from django.urls import path
from users.views import register_view, login_view, activate_account
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
]