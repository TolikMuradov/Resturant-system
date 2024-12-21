from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Listede görüntülenecek alanlar
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)

    # Read-only alanlar
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')

    def has_add_permission(self, request, obj=None):
        """Yeni mesaj eklenmesini engeller."""
        return False

    def has_change_permission(self, request, obj=None):
        """Mevcut mesajların düzenlenmesini engeller."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Silme işlemini izin verir."""
        return True