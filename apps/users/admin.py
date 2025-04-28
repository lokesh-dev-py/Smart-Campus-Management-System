from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
# Register your models here.

@admin.register(User)
class UserModelAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'is_staff', 'is_active', 'is_teacher', 'is_student']
    list_filter = ['is_superuser']
    fieldsets = [
        ('User Credentials', {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['name']}),
        ('Permissions', {'fields': ['is_staff', 'is_active', 'is_teacher', 'is_student']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        )
    ]
    search_fields = ['email']
    ordering = ['email','id']
    filter_horizontal = []

