from django.db import models
from transliterate import translit
from django.urls import reverse
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):

    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение (превью)', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} - {self.price}: {self.category}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ('name',)


class Record(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, unique=True,  verbose_name='Slug')
    content = models.CharField(max_length=500, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='records/', **NULLABLE, verbose_name='Превью (изображение)')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = translit(self.title, 'ru', reversed=True)
            self.slug = slugify(transliterated_title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog_app:record_detail', kwargs={'slug': self.slug})

    def toggle_published(self):
        self.published = not self.published
        self.save()


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.CharField(max_length=20, verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(verbose_name='Признак текущей версии')

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    def __str__(self):
        return self.name
