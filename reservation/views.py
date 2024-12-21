from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings

def make_reservation(request):
    if request.method == "POST":
        # Formdan gelen verileri işleme
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        time = request.POST.get("time")
        guests = request.POST.get("guests")

        if not (name and email and date and time and guests):
            messages.error(request, "Tüm alanları doldurun!")
            return redirect("make_reservation")

        # Yeni rezervasyon oluştur
        reservation = Reservation.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            guests=guests,
            user=request.user if request.user.is_authenticated else None,
        )

        # E-posta gönderme işlemi
        try:
            send_mail(
                subject="Rezervasyon Onayı",
                message=(
                    f"Merhaba {name},\n\n"
                    f"Rezervasyonunuz başarıyla alındı.\n"
                    f"Tarih: {date}\n"
                    f"Saat: {time}\n"
                    f"Misafir Sayısı: {guests}\n\n"
                    "Sizi restoranımızda görmekten mutluluk duyacağız.\n\n"
                    "Teşekkürler,\nRestaurant Ekibi"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "Rezervasyon başarıyla oluşturuldu! E-posta gönderildi.")
        except Exception as e:
            messages.warning(request, f"Rezervasyon oluşturuldu ancak e-posta gönderilemedi. Hata: {str(e)}")

        return redirect("profile")  # Profil sayfasına yönlendir
    else:
        # GET isteği için bir sayfa render et
        return render(request, "reservation/make_reservation.html")


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'reservation/my_reservations.html', {'reservations': reservations})