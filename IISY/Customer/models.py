from django.db import models
from django.conf import settings
from django_tenants.models import TenantMixin, DomainMixin

# Models for different Clients, in this case our customers
# Need to study this further


class Client(TenantMixin):
    SUBSCRIPTION_MODEL = (
        ('50', 'Standard'),
        ('150', 'Premium')
    )

    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=10)
    subscription = models.CharField(max_length=10, choices=SUBSCRIPTION_MODEL, default=SUBSCRIPTION_MODEL[0][0], blank=True)
    auto_drop_schema = True


class Domain(DomainMixin):
    pass