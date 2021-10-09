from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    list_display = ['phone', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )
    search_fields = ['phone']
    ordering = ['phone']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
