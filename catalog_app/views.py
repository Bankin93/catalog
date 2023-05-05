from django.shortcuts import render

from catalog_app.models import Product, Contact


# Create your views here.


def home(request):
    latest_products = Product.objects.order_by('-created_date')[:5]
    for product in latest_products:
        print(product.name)
    return render(request, 'catalog_app/home.html', {'latest_products': latest_products})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, phone=phone, message=message)
        contact.save()
        print(f'You have new message from {name}({phone}): {message}')
        return render(request, 'catalog_app/feedback.html')
    else:
        contacts_info = Contact.objects.all()
        return render(request, 'catalog_app/contacts.html', {'contacts_info': contacts_info})

