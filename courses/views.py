from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Category

def course_list(request):
    courses = Course.objects.filter(is_published=True)
    categories = Category.objects.all()
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories
    })

def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    related_courses = Course.objects.filter(
        category=course.category,
        is_published=True
    ).exclude(id=course.id)[:3]
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'related_courses': related_courses
    })

@login_required
def enroll_course(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    
    # Check if user is already enrolled
    if request.user.enrollments.filter(course=course).exists():
        return redirect('my_courses')
    
    # Create enrollment
    enrollment = request.user.enrollments.create(
        course=course,
        status='pending'
    )
    
    # Redirect to payment
    return redirect('checkout', course_id=course.id)

@login_required
def course_trial(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    
    if not course.has_trial:
        return redirect('course_detail', course_slug=course_slug)
    
    # Get first free lesson
    first_lesson = course.modules.first().lessons.filter(is_free=True).first()
    
    if not first_lesson:
        return redirect('course_detail', course_slug=course_slug)
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': first_lesson
    })

@login_required
def my_courses(request):
    enrollments = request.user.enrollments.filter(status='active')
    return render(request, 'courses/my_courses.html', {
        'enrollments': enrollments
    })
