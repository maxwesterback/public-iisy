from django.urls import path, include
from django.conf.urls import url
from iisy_landing import views

urlpatterns = [
    path('', views.company_page, name='company_page'),
]
