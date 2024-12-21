from django.shortcuts import render

def reservation_form(request):
    return render(request, 'reservation/form.html')

def reservation_success(request):
    return render(request, 'reservation/success.html')
