# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('category/<slug:category_slug>/', views.course_list_by_category, name='course_list_by_category'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('<slug:course_slug>/trial/', views.course_trial, name='course_trial'),
    path('my-courses/', views.my_courses, name='my_courses'),
]