from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Mesajı kaydet
        ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)

        # Başarılı geri bildirim mesajı
        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')  # Ana sayfaya yönlendirme

    return render(request, 'home/index.html')  # Formun bulunduğu sayfa

