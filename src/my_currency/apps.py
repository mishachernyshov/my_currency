from django.contrib.admin.apps import AdminConfig


class MyCurrencyConfig(AdminConfig):
    default_site = 'my_currency.admin.MyCurrencyAdminSite'
