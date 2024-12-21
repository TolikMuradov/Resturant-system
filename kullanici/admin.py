from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Notification

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone', 'created_at', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('get_users', 'title', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message')
    filter_horizontal = ('user',)  # Çoklu kullanıcı seçimi için
    fields = ('user', 'title', 'message', 'is_read')

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.user.all()])
    get_users.short_description = 'Users'  # Admin panelinde başlık olarak ne gözükecek