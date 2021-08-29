from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from . import views


urlpatterns = [
    path('', views.company_page, name='index'),
    path('v1/api/department/', views.DepartmentListCreate.as_view()),
    path('v1/api/department/<int:pk>', views.SingleDepartmentView.as_view()),
    path('v1/api/entity/', views.EntityListCreate.as_view()),
    path('v1/api/entity/<int:pk>', views.SingleEntityView.as_view()),
    path('v1/api/ticket/', views.TicketListCreate.as_view()),
    path('v1/api/ticket/<int:pk>', views.SingleTicketView.as_view()),
    path('<str:object_uuid>', views.landing, name='customer_page'),
    path('new_ticket/', views.register_ticket, name='new_ticket'),
    path('dashboard/', views.Graph.as_view(), name='home'),
]
