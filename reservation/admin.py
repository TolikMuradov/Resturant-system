from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'guests')
    readonly_fields = ('name', 'email', 'phone', 'date', 'time', 'guests')
    search_fields = ('name', 'email', 'date')
    list_filter = ('date', 'time')

    def has_add_permission(self, request, obj=None):
        return False  # Yalnızca görüntüleme ve silme izni
