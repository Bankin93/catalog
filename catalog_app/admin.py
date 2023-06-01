from django.contrib import admin

from catalog_app.models import Category, Product, Contact, Record, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    search_fields = ('name', 'phone')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content', 'preview', 'published')
    prepopulated_fields = {"slug": ("title",)}

    def republish(self, request, queryset):
        queryset.update(published=True)
        self.message_user(request, "Выбранные записи были переизданы")

    republish.short_description = "Повторная публикация выбранных записей"
    actions = [republish]


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'name', 'is_active',)

