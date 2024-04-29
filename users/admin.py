from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    list_display = ['email', 'phone', 'city', 'is_staff']
    search_fields = ('email', 'phone')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
