from django.contrib import admin
from django.urls import path, include
from account import views

urlpatterns = [
    path('', views.customers),
    path('<int:customer_id>/clean_cart/', views.clean_cart),
    path('<int:customer_id>/buy/', views.buy),
    path('<int:customer_id>/', views.customer_edit),

]