from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, TableAvailability
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Reservation)
def send_reservation_status_email(sender, instance, **kwargs):
    # Sadece durum güncellemelerinde e-posta gönder
    if 'status' in instance.__dict__ and instance.status in ['approved', 'cancelled']:
        email_subject = ""
        email_message = ""

        if instance.status == "approved":
            email_subject = "Rezervasyon Onaylandı"
            email_message = (
                f"Merhaba {instance.name},\n\n"
                f"Rezervasyonunuz onaylanmıştır.\n"
                f"Tarih: {instance.date}\n"
                f"Saat: {instance.time}\n"
                f"Misafir Sayısı: {instance.guests}\n\n"
                "Sizi restoranımızda görmekten mutluluk duyacağız.\n\n"
                "Teşekkürler,\nRestaurant Ekibi"
            )
        elif instance.status == "cancelled":
            email_subject = "Rezervasyon İptal Edildi"
            email_message = (
                f"Merhaba {instance.name},\n\n"
                f"Rezervasyonunuz iptal edilmiştir.\n"
                f"Tarih: {instance.date}\n"
                f"Saat: {instance.time}\n\n"
                "Başka bir zaman sizi restoranımızda ağırlamak isteriz.\n\n"
                "Teşekkürler,\nRestaurant Ekibi"
            )

        # E-posta gönderimi
        try:
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"E-posta gönderimi başarısız: {str(e)}")


@receiver(post_save, sender=Reservation)
def update_table_status(sender, instance, **kwargs):
    """
    Rezervasyon durumu güncellendiğinde masa durumu ve uygunluk bilgilerini düzenle.
    """
    if instance.status == "cancelled" and instance.table:
        # Masayı boşalt
        instance.table.is_available = True
        instance.table.save()

        # Uygunluk bilgisini temizle
        TableAvailability.objects.filter(
            table=instance.table,
            date=instance.date,
            start_time=instance.time,
        ).delete()

@receiver(post_delete, sender=Reservation)
def clear_availability_on_delete(sender, instance, **kwargs):
    """
    Rezervasyon silindiğinde uygunluk bilgisini temizle.
    """
    if instance.table:
        instance.table.is_available = True
        instance.table.save()
        TableAvailability.objects.filter(
            table=instance.table,
            date=instance.date,
            start_time=instance.time,
        ).delete()