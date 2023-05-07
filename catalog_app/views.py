from django.shortcuts import render

from catalog_app.models import Product, Contact, Category


def home(request):
    latest_products = Product.objects.order_by('-created_date')[:5]
    for products in latest_products:
        print(products.name)
    context = {
        'object_list': Product.objects.all(),
        'category_list': Category.objects.all()
    }
    return render(request, 'catalog_app/home.html', context)


def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        'object': product_item,
        'title': product_item.name
    }
    return render(request, 'catalog_app/product.html', context)


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

