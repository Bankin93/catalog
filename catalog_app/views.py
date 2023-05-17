from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog_app.models import Product, Contact, Category, Record
from catalog_app.services import send_register_mail


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class RecordListView(ListView):
    model = Record
    queryset = Record.objects.filter(published=True)


class RecordCreateView(CreateView):
    model = Record
    fields = ('title', 'content', 'preview', 'published')
    success_url = reverse_lazy('catalog_app:record_list')


class RecordUpdateView(UpdateView):
    model = Record
    fields = ('title', 'slug', 'content', 'preview', 'published', 'views_count')

    def get_success_url(self):
        return self.object.get_absolute_url()


class RecordDetailView(DetailView):
    model = Record

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        if obj.views_count == 3:
            send_register_mail(obj, settings.EMAIL_HOST_USER)
        obj.save()
        return obj


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('catalog_app:record_list')


def toggle_activity(request, slug):
    record_item = get_object_or_404(Record, slug=slug)
    record_item.toggle_published()
    return redirect(reverse('catalog_app:record_detail', args=[record_item.slug]))


class ContactCreateView(CreateView):
    template_name = 'catalog_app/contacts.html'

    def get(self, request, *args, **kwargs):
        contacts_info = Contact.objects.all()
        return render(request, self.template_name, {'contacts_info': contacts_info})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, phone=phone, message=message)
        contact.save()
        print(f'You have new message from {name}({phone}): {message}')
        return render(request, 'catalog_app/feedback.html')
