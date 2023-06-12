from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog_app.apps import CatalogAppConfig
from catalog_app.views import ProductListView, ContactCreateView, ProductDetailView, RecordListView, RecordDetailView, \
    RecordCreateView, RecordUpdateView, RecordDeleteView, toggle_activity, ProductCreateView, ProductDeleteView, \
    ProductUpdateView, ProductCategoryUpdateView, ProductDescriptionUpdateView, change_is_published, CategoryListView

app_name = CatalogAppConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', never_cache(ContactCreateView.as_view()), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('product_create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('product_update/<int:pk>', never_cache(ProductUpdateView.as_view()), name='product_update'),
    path('product_update_description/<int:pk>/', never_cache(ProductDescriptionUpdateView.as_view()),
         name='product_description'),
    path('product_update_category/<int:pk>/', never_cache(ProductCategoryUpdateView.as_view()),
         name='product_category'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('is_published/<int:pk>/', change_is_published, name='change_is_published'),
    path('records/', RecordListView.as_view(), name='record_list'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('records_create/', never_cache(RecordCreateView.as_view()), name='create_record'),
    path('records_update/<slug:slug>/', never_cache(RecordUpdateView.as_view()), name='update_record'),
    path('records_delete/<slug:slug>/', RecordDeleteView.as_view(), name='delete_record'),
    path('toggle/<slug:slug>/', toggle_activity, name='toggle_activity')

]
