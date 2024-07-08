from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


def update_queries_action(modeladmin, request, queryset):
    for user in queryset:
        if user.subscription_type == 'INSIGHT':
            user.queries = 50
        elif user.subscription_type == 'PROFESSIONAL':
            user.queries = 500
        elif user.subscription_type == 'PROFESSIONAL_PLUS':
            user.queries = 2000
        elif user.subscription_type == 'ENTERPRISE':
            user.queries = 5000

        user.save()
    modeladmin.message_user(request, "Queries updated successfully.")

update_queries_action.short_description = "Update User Queries"
class UserAdmin(BaseUserAdmin):
    actions = [update_queries_action]
    list_display = ('email', 'full_name', 'account_name', 'phone_number', 'product_key', 'subscription_type', 'stripe_subscription_id', 'subscription_active', 'queries', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ('product_key',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'account_name', 'phone_number')}),
        ('Product info', {'fields': ('product_key', 'subscription_type', 'stripe_subscription_id', 'queries', 'subscription_active', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'account_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
