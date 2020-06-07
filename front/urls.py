from django.urls import path
from .import views

urlpatterns = [
    path('', views.index,name='home'),
    path('home_two', views.home_two,name='home_two'),
    path('course_list', views.course_list,name='course_list'),
    path('testing_file', views.testing_file,name='testing_file'),
    path('course_details/<slug:slug>', views.course_details,name='course_details'),
    path('course_details_2', views.course_details_2,name='course_details_2'),
    # path('instructor_singup', views.instructor_singup,name='instructor_singup'),
    path('instructor_logout', views.instructor_logout,name='instructor_logout'),
    path('logout', views.dologout,name='dologout'),
    path('about_us', views.about_us,name='about_us'),
    path('career', views.career,name='career'),
    path('contact_us', views.contact_us,name='contact_us'),
]
