from catalog_app.apps import CatalogAppConfig
from django.urls import path
from catalog_app.views import home, contacts

app_name = CatalogAppConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('contacts/feedback/', contacts, name='contacts')
]
