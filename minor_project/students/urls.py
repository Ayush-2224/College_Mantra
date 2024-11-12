
from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.option, name='register'),


    # Student URLs
    path('student/signup/', views.student_signup, name='student_signup'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/home/', views.student_home, name='student_home'),
    path('', views.home, name='home'),

    # College URLs
    path('college/signup/', views.college_signup, name='college_signup'),
    path('college/login/', views.college_login, name='college_login'),
    path('college/logout/', views.college_logout, name='college_logout'),
    path('college/register/', views.college_register, name='college_register'),
    path('college/home/', views.college_home, name='college_home'),
    # path('', views.home, name='common_home'),
    
    path('add_preference/<int:college_id>/<int:course_id>/', views.add_preference, name='add_preference'),
    path('remove_preference/<int:college_id>/<int:course_id>/', views.remove_preference, name='remove_preference'),
    path('list/', views.college_course_view, name='list'),
    # path('preferences/', views.remove, name='preferences'),

    # path('allocate/',views.allocate_colleges,name='allocate'),
]
