from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Table(models.Model):
    SEAT_CHOICES = [
        (2, "2 Kişilik"),
        (4, "4 Kişilik"),
        (6, "6 Kişilik"),
        (8, "8 Kişilik"),
    ]

    number = models.PositiveIntegerField(unique=True, default=1)  # Masa numarası
    seats = models.PositiveIntegerField(choices=SEAT_CHOICES, default=2)  # Koltuk sayısı
    is_available = models.BooleanField(default=True)  # Boş/Dolu durumu

    def __str__(self):
        return f"Masa {self.number} - {self.get_seats_display()}"


class TableAvailability(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.table} ({self.date} - {self.start_time} - {self.end_time})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylanmış'),
        ('cancelled', 'İptal Edilmiş'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)  # Yeni alan

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"

    def delete(self, *args, **kwargs):
        # Hard delete işlemi
        super().delete(*args, **kwargs)