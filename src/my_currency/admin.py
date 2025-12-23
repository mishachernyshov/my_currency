from django.contrib import admin
from django.urls import path

from core import views as core_views


class MyCurrencyAdminSite(admin.AdminSite):
    site_header = 'My Currency Administration'
    site_title = 'My Currency site admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('currency-converter/', core_views.currency_converter_view, name='currency-converter'),
        ]
        return custom_urls + urls


admin_site = MyCurrencyAdminSite(name='my_currency_admin')
