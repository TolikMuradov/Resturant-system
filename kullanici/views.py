from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Form doğrulama işlemleri
        if password1 != password2:
            messages.error(request, "Şifreler eşleşmiyor.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Bu e-posta adresi zaten kullanılıyor.")
        else:
            # Kullanıcı oluşturma
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, "Başarıyla kayıt oldunuz.")
            return redirect('home')

    return render(request, 'kullanici/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Başarıyla giriş yaptınız.")
            return redirect('home')
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")

    return render(request, 'kullanici/login.html')


def profile(request):
    return render(request, 'kullanici/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    messages.info(request, "Çıkış yaptınız.")
    return redirect('home')
