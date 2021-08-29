from django.db import models
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from Customer.models import Client


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name',)
