
from catalog_app.apps import CatalogAppConfig
from django.urls import path
from catalog_app.views import home, contacts, product

app_name = CatalogAppConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('contacts/feedback/', contacts, name='contacts'),
    path('product/<int:pk>/', product, name='product')
]
