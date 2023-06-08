from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog_app.forms import ProductForm, VersionForm, ProductDescriptionForm, ProductCategoryForm
from catalog_app.models import Product, Contact, Category, Record, Version
from catalog_app.services import send_register_mail


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('catalog_app.set_published_product'):
            return queryset
        return queryset.filter(is_published=True)


@permission_required('catalog_app.set_published_product')
def change_is_published(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    product_item.toggle_is_published()
    return redirect(reverse('catalog_app:product_detail', args=[product_item.pk]))


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_published or self.request.user.has_perm('catalog_app:change_description_product'):
            return self.object
        raise HttpResponseForbidden


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog_app:product_list')

    def form_valid(self, form):
        product = form.save()
        product.user = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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


class ProductDescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductDescriptionForm
    template_name = 'catalog_app/product_description.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('catalog_app:product_detail', kwargs={'pk': pk})

    def test_func(self):
        return self.request.user.has_perm(perm='catalog_app.change_description_product')


class ProductCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCategoryForm
    template_name = 'catalog_app/product_category.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('catalog_app:product_detail', kwargs={'pk': pk})

    def test_func(self):
        return self.request.user.has_perm(perm='catalog_app.change_product_category')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog_app:product_list')

    def test_func(self):
        return self.request.user.has_perm(perm='catalog_app.product_delete')


class RecordListView(ListView):
    model = Record
    queryset = Record.objects.filter(published=True)


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    fields = ('title', 'content', 'preview', 'published')
    success_url = reverse_lazy('catalog_app:record_list')


class RecordUpdateView(LoginRequiredMixin, UpdateView):
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


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Record
    success_url = reverse_lazy('catalog_app:record_list')


def toggle_activity(request, slug):
    record_item = get_object_or_404(Record, slug=slug)
    record_item.toggle_published()
    return redirect(reverse('catalog_app:record_detail', args=[record_item.slug]))


class ContactCreateView(LoginRequiredMixin, CreateView):
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
