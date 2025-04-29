# courses/models.py
from django.db import models
from users.models import CustomUser
from django.db.models import Count, Case, When, IntegerField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    LEVELS = (
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    level = models.CharField(max_length=15, choices=LEVELS)
    image = models.ImageField(upload_to='course_images/')
    video_intro = models.FileField(upload_to='course_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    has_trial = models.BooleanField(default=False, help_text="Kursda bepul sinov darsi mavjudmi?")
    
    def __str__(self):
        return self.title

    def get_discount_percentage(self):
        if self.discount_price and self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def get_level_display(self):
        return dict(self.LEVELS)[self.level]
    
    @property
    def total_duration(self):
        total = sum(module.duration for module in self.modules.all())
        return f"{total} soat"
    
    @property
    def learning_outcomes(self):
        return [
            "Trading asoslarini o'rganish",
            "Texnik tahlil metodlarini o'zlashtirish",
            "Risk menejmentini o'rganish",
            "Trading strategiyalarini ishlab chiqish"
        ]
    
    @property
    def requirements(self):
        return [
            "Kompyuter va internet ulanishi",
            "Trading haqida boshlang'ich bilim",
            "Risk olishga tayyorlik"
        ]
    
    @property
    def target_audience(self):
        return [
            "Tradingni o'rganishni istovchilar",
            "Tajribali treyderlar",
            "Moliyaviy bozorlar bilan qiziqadiganlar"
        ]
    
    @property
    def ratings_distribution(self):
        distribution = self.reviews.aggregate(
            five_stars=Count(Case(When(rating=5, then=1), output_field=IntegerField())),
            four_stars=Count(Case(When(rating=4, then=1), output_field=IntegerField())),
            three_stars=Count(Case(When(rating=3, then=1), output_field=IntegerField())),
            two_stars=Count(Case(When(rating=2, then=1), output_field=IntegerField())),
            one_star=Count(Case(When(rating=1, then=1), output_field=IntegerField()))
        )
        total = sum(distribution.values())
        if total == 0:
            return {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        return {
            5: int((distribution['five_stars'] / total) * 100),
            4: int((distribution['four_stars'] / total) * 100),
            3: int((distribution['three_stars'] / total) * 100),
            2: int((distribution['two_stars'] / total) * 100),
            1: int((distribution['one_star'] / total) * 100)
        }

    @property
    def video_count(self):
        return self.lessons.filter(type='video').count()

    @property
    def text_count(self):
        return self.lessons.filter(type='text').count()

    @property
    def quiz_count(self):
        return self.lessons.filter(type='quiz').count()

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    duration = models.IntegerField(default=0, help_text="Modul davomiyligi soatlarda")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    LESSON_TYPES = (
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    type = models.CharField(max_length=20, choices=LESSON_TYPES, default='video')
    order = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('active', 'Faol'),
        ('completed', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"