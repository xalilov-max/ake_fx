# payments/models.py
from django.db import models
from users.models import CustomUser
from courses.models import Course

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('card', 'Karta'),
        ('transfer', 'Bank o\'tkazmasi'),
        ('cash', 'Naqd pul'),
        ('click', 'Click'),
        ('payme', 'Payme'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('completed', 'To\'langan'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('refunded', 'Qaytarilgan'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.amount}"