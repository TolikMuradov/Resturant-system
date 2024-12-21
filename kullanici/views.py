from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import make_password
from utils.send_email import send_html_email
from utils.token_generator import token_generator
from django.contrib.auth.tokens import default_token_generator
from .forms import ProfileUpdateForm
from django import forms
from .models import CustomUser
from reservation.models import Reservation
from utils.send_email import send_html_email  # Ekledik
from .models import Notification
from utils.notifications import send_notification
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from menu.models import Order
import json
from django.contrib.auth.models import AnonymousUser

try:
    from django.utils.encoding import force_str
except ImportError:
    from django.utils.encoding import force_text as force_str


User = get_user_model()
token_generator = PasswordResetTokenGenerator()

import re

def is_password_strong(password):
    """
    Şifre politikası:
    - En az 8 karakter
    - En az bir büyük harf
    - En az bir küçük harf
    - En az bir rakam
    - En az bir özel karakter
    """
    if len(password) < 8:
        return False, "Şifre en az 8 karakter olmalıdır."
    if not re.search(r'[A-Z]', password):
        return False, "Şifre en az bir büyük harf içermelidir."
    if not re.search(r'[a-z]', password):
        return False, "Şifre en az bir küçük harf içermelidir."
    if not re.search(r'\d', password):
        return False, "Şifre en az bir rakam içermelidir."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Şifre en az bir özel karakter içermelidir."
    return True, "Şifre güçlü."

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Şifreler eşleşmiyor.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Bu e-posta adresi zaten kullanılıyor.")
        else:
            # Şifre politikası kontrolü
            is_strong, message = is_password_strong(password1)
            if not is_strong:
                messages.error(request, message)
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.is_email_verified = False
                    user.save()

                    # Doğrulama e-postası gönder
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    verification_link = request.build_absolute_uri(
                        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
                    )
                    send_html_email(
                        subject="E-posta Doğrulama",
                        to_email=email,
                        template='email/verify_email.html',
                        context={'user': user, 'verification_link': verification_link}
                    )
                    messages.success(request, "Kayıt başarılı. Lütfen e-postanızı doğrulayın.")
                    return redirect('home')
                except Exception as e:
                    messages.error(request, f"Bir hata oluştu: {str(e)}")

    return render(request, 'kullanici/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_email_verified:
                messages.error(request, "E-postanızı doğrulamanız gerekiyor.")
                return redirect('login')
            login(request, user)
            messages.success(request, f"Başarıyla giriş yaptınız. Hoş geldiniz, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")

    return render(request, 'kullanici/login.html')


def profile_view(request):
    if isinstance(request.user, AnonymousUser):
        messages.error(request, "Profil sayfasını görüntülemek için giriş yapmalısınız.")
        return redirect('login')

    reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-time')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Siparişleri alın
    unread_notifications_exist = request.user.notifications.filter(is_read=False).exists()

    return render(request, 'kullanici/profile.html', {
        'reservations': reservations,
        'orders': orders,
        'unread_notifications_exist': unread_notifications_exist,
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Çıkış yaptınız.")
    return redirect('home')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/kullanici/reset-password/{uid}/{token}/')

            send_html_email(
                subject="Şifre Sıfırlama Talebi",
                to_email=email,
                template='email/forgot_password.html',
                context={'reset_link': reset_link, 'user': user}
            )
            messages.success(request, "Şifre sıfırlama talimatları e-posta adresinize gönderildi.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Bu e-posta adresine sahip bir kullanıcı bulunamadı.")

    return render(request, 'kullanici/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Şifreniz başarıyla sıfırlandı.')
                return redirect('login')
            else:
                messages.error(request, 'Şifreler uyuşmuyor.')
        return render(request, 'kullanici/reset_password.html', {'validlink': True})
    else:
        return render(request, 'kullanici/reset_password.html', {'validlink': False})
    

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'kullanici/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        messages.success(request, "Bildirim okundu olarak işaretlendi.")
    except Notification.DoesNotExist:
        messages.error(request, "Bildirim bulunamadı.")
    return redirect('notifications')

@login_required
def navbar_context(request):
    unread_notifications_exist = request.user.notifications.filter(is_read=False).exists()
    return {'unread_notifications_exist': unread_notifications_exist}


@login_required
def mark_as_read_and_delete(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()  # Bildirimi sil
    return HttpResponseRedirect(reverse('notifications'))  # Bildirimler sayfasına yönlendir


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()

        # Kullanıcıyı otomatik giriş yapmış hale getirme
        login(request, user)

        messages.success(request, "E-postanız başarıyla doğrulandı ve giriş yaptınız.")
        return redirect('home')
    else:
        messages.error(request, "E-posta doğrulama bağlantısı geçersiz.")
        return redirect('home')

@login_required
def delete_account(request):
    """
    Kullanıcının hesabını tamamen siler.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()  # Kullanıcıyı tamamen sil
        messages.success(request, "Hesabınız başarıyla silindi.")
        return redirect('home')  # Ana sayfaya yönlendirme
    return redirect('profile')  # POST değilse profile yönlendirme