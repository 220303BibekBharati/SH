from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    actions = ['deactivate_users', 'delete_users_permanently']

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {updated} user(s).")
    deactivate_users.short_description = 'Deactivate selected users'

    def delete_users_permanently(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Permanently deleted {count} user(s).")
    delete_users_permanently.short_description = 'Delete selected users permanently'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)