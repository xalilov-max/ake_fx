# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:course_id>/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]