from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reservation, Table, TableAvailability
from django.contrib.auth.decorators import login_required

from utils.send_email import send_html_email
from django.conf import settings
from datetime import datetime, timedelta

from django.utils.timezone import localtime

def make_reservation(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        time = request.POST.get("time")  # Saat formatı 'HH:MM'
        guests = int(request.POST.get("guests"))
        table_id = request.POST.get("table")

        # Eksik alan kontrolü
        if not all([name, email, date, time, guests, table_id]):
            messages.error(request, "Tüm alanları doldurun!")
            return redirect("make_reservation")

        # Masa kontrolü
        table = get_object_or_404(Table, id=table_id)
        start_time = datetime.strptime(time, "%H:%M").time()
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time()

        conflicts = TableAvailability.objects.filter(
            table=table,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if conflicts.exists():
            messages.error(request, "Seçilen masa bu saat aralığında dolu.")
            return redirect("make_reservation")

        # Rezervasyon oluştur
        reservation = Reservation.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=start_time,
            guests=guests,
            table=table,
            user=request.user if request.user.is_authenticated else None,
        )

        # Masa uygunluk bilgisi ekle
        TableAvailability.objects.create(
            table=table,
            date=date,
            start_time=start_time,
            end_time=end_time,
        )

        # Masa durumu güncelle
        table.is_available = False
        table.save()

        # E-posta gönderimi
        try:
            send_html_email(
                subject="Rezervasyon Onayı",
                to_email=email,
                template="email/reservation_confirmation.html",
                context={"reservation": reservation},
            )
        except Exception as e:
            messages.warning(request, f"E-posta gönderilemedi: {str(e)}")

        messages.success(request, "Rezervasyon başarıyla oluşturuldu!")
        return redirect("profile")

    # GET isteği: uygun masaları getir
    available_tables = Table.objects.all()
    return render(request, "reservation/make_reservation.html", {"tables": available_tables})



@login_required
def reservation_list(request):
    if not request.user.is_staff:
        messages.error(request, "Bu sayfaya erişim izniniz yok.")
        return redirect('home')

    status_filter = request.GET.get('status', 'all')
    reservations = Reservation.objects.all().order_by('-date', '-time')

    if status_filter != 'all':
        reservations = reservations.filter(status=status_filter)

    return render(request, 'reservation/reservation_list.html', {
        'reservations': reservations,
        'status_filter': status_filter,
    })

@login_required
def update_reservation_status(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        messages.error(request, "Rezervasyon bulunamadı.")
        return redirect('reservation_list')

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status not in dict(Reservation.STATUS_CHOICES):
            messages.error(request, "Geçersiz durum.")
            return redirect('reservation_list')

        reservation.status = new_status
        reservation.save()

        # Masa boşaltma işlemi
        if new_status == "cancelled" and reservation.table:
            reservation.table.is_available = True
            reservation.table.save()

        # E-posta içeriği ve gönderimi
        subject, template = "", ""
        if new_status == "approved":
            subject = "Rezervasyon Onaylandı"
            template = "email/reservation_approved.html"
        elif new_status == "cancelled":
            subject = "Rezervasyon İptal Edildi"
            template = "email/reservation_cancelled.html"

        if subject and template:
            try:
                send_html_email(
                    subject=subject,
                    to_email=reservation.email,
                    template=template,
                    context={"reservation": reservation}
                )
                messages.success(request, "Rezervasyon durumu güncellendi ve e-posta gönderildi.")
            except Exception as e:
                messages.warning(request, f"E-posta gönderilemedi: {str(e)}")

        return redirect('reservation_list')

    return render(request, "reservation/update_status.html", {"reservation": reservation})
