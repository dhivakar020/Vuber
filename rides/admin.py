from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Define fields for the admin interface
    list_display = ('id', 'role', 'created_at', 'updated_at')  # Adjust fields as per your model
    list_filter = ('role',)
    ordering = ('id',)  # Adjust ordering field
    search_fields = ('id',)  # Adjust as needed

    # Define fieldsets for adding and editing users
    fieldsets = (
        (None, {'fields': ('id', 'role', 'password')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    # Define fields for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('role', 'password1', 'password2'),
        }),
    )

# Register the custom user model and UserAdmin
admin.site.register(User, UserAdmin)
