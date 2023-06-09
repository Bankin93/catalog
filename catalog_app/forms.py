from django import forms

from catalog_app.models import Product, Version, Record

FORBIDDEN_WORDS = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in FORBIDDEN_WORDS:
            raise forms.ValidationError('Запрещенное название')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data in FORBIDDEN_WORDS:
            raise forms.ValidationError('Запрещенное описание')
        return cleaned_data


class VersionForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def clean_is_active(self):
        cleaned_data = self.cleaned_data['is_active']
        if cleaned_data and self.instance.product.version_set.filter(is_active=True).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError('Может существовать только одна активная версия.')
        return cleaned_data


class ProductDescriptionForm(ProductForm):
    class Meta:
        model = Product
        fields = ('description', )


class ProductCategoryForm(ProductForm):
    class Meta:
        model = Product
        fields = ('category',)


class RecordForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Record
        exclude = ('slug', 'views_count', )
