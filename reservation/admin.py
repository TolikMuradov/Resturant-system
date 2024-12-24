# reservation/admin.py
from django.contrib import admin
from .models import Reservation, Table, TableAvailability

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats', 'is_available')
    list_filter = ('is_available', 'seats')
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'guests', 'status', 'table')
    list_filter = ('status', 'date', 'time')
    search_fields = ('name', 'email', 'phone')
    actions = ['approve_reservations', 'cancel_reservations']

    def delete_queryset(self, request, queryset):
        # Tüm seçili nesneleri hard delete ile sil
        for obj in queryset:
            obj.delete()


    def approve_reservations(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} rezervasyon onaylandı.")
    approve_reservations.short_description = "Seçilen rezervasyonları onayla"

    def cancel_reservations(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} rezervasyon iptal edildi.")
    cancel_reservations.short_description = "Seçilen rezervasyonları iptal et"


@admin.register(TableAvailability)
class TableAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('table', 'date', 'start_time', 'end_time')
    list_filter = ('date', 'table')