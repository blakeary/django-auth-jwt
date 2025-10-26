from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, VerifyEmailToken


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_email_verified', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_email_verified', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Email verification', {'fields': ('is_email_verified', 'pending_email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    readonly_fields = ['date_joined', 'last_login']


class VerifyEmailTokenAdmin(admin.ModelAdmin):
    model = VerifyEmailToken
    list_display = ['user', 'token_type', 'is_used', 'created_at', 'expires_at', 'is_valid_status']
    list_filter = ['token_type', 'is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at']
    ordering = ['-created_at']

    def is_valid_status(self, obj):
        return obj.is_valid()

    is_valid_status.boolean = True
    is_valid_status.short_description = 'Valid'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerifyEmailToken, VerifyEmailTokenAdmin)