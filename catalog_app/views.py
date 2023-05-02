from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'catalog_app/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}): {message}')
        return render(request, 'catalog_app/feedback.html')
    else:
        return render(request, 'catalog_app/contacts.html')

