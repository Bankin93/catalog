from django.conf import settings
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog_app.forms import ProductForm, VersionForm
from catalog_app.models import Product, Contact, Category, Record, Version
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog_app:product_list')

    def form_valid(self, form):
        product = form.save()
        product.user = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog_app:product_list')
    template_name = 'catalog_app/product_from_with_version.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog_app:product_list')


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
        if obj.views_count == 100:
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
