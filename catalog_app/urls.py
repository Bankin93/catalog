from django.urls import path

from catalog_app.apps import CatalogAppConfig
from catalog_app.views import ProductListView, ContactCreateView, ProductDetailView, RecordListView, RecordDetailView, \
    RecordCreateView, RecordUpdateView, RecordDeleteView, toggle_activity, ProductCreateView, ProductDeleteView, \
    ProductUpdateView

app_name = CatalogAppConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactCreateView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('records/', RecordListView.as_view(), name='record_list'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('records_create/', RecordCreateView.as_view(), name='create_record'),
    path('records_update/<slug:slug>/', RecordUpdateView.as_view(), name='update_record'),
    path('records_delete/<slug:slug>/', RecordDeleteView.as_view(), name='delete_record'),
    path('toggle/<slug:slug>/', toggle_activity, name='toggle_activity')

]
