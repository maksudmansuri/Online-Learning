from django.urls import path
from .import views

urlpatterns = [
    path('', views.counsellor_dashboard,name='counsellor_dashboard'),
    path('manage_staff', views.manage_staff,name='manage_staff'),
    path('staff_activate/<id>', views.staff_activate,name='staff_activate'),
    path('staff_deactivate/<id>', views.staff_deactivate,name='staff_deactivate'),

    path('manage_student', views.manage_student,name='manage_student'),
    path('student_activate/<id>', views.student_activate,name='student_activate'),
    path('student_deactivate/<id>', views.student_deactivate,name='student_deactivate'),

    path('course_activate/<slug>', views.course_activate,name='course_activate'),
    path('course_deactivate/<slug>', views.course_deactivate,name='course_deactivate'),
    path('manage_course', views.manage_course,name='manage_student'),
    path('check_course_session_activate/<slug>/<sslug>/<ssslug>', views.check_course_session_activate,name='check_course_session_activate'),
    path('check_course_session_deactivate/<slug>/<sslug>/<ssslug>', views.check_course_session_deactivate,name='check_course_session_deactivate'),
    
    path('course_category', views.course_category,name='course_category'),
    path('course_subcategory/<id>', views.course_subcategory,name='course_subcategory'),
    path('course_category_delete/<id>', views.course_category_delete,name='course_category_delete'),
    path('course_subcategory_delete/<sid>/<id>', views.course_subcategory_delete,name='course_subcategory_delete'),

    path('check_course_details/<slug>', views.check_course_details,name='check_course_details'),
    path('check_course_session/<slug>/<sslug>/<ssslug>', views.check_course_session,name='check_course_session'),

    path('counsellor_login', views.counsellor_login,name='counsellor_login'),
    # path('counsellor_singup', views.counsellor_singup,name='counsellor_singup'),
    path('counsellor_logout', views.counsellor_logout,name='counsellor_logout')
]