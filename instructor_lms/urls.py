from django.urls import path,include
from .import views
 
urlpatterns = [
    path('',views.instructor_dashboard,name='instructor_dashboard'),
    path('instructor_account_edit_save',views.instructor_account_edit_save,name='instructor_account_edit_save'),
    path('instructor_account_edit',views.instructor_account_edit,name='instructor_account_edit'),
    
    path('instructor_course_edit/<slug:slug>',views.instructor_course_edit,name='instructor_course_edit'),
    path('instructor_courses',views.instructor_courses,name='instructor_courses'),
    path('instructor_course_add_save',views.instructor_course_add_save,name='instructor_course_add_save'),
    path('instructor_course_add',views.instructor_course_add,name='instructor_course_add'),
    
    path('instructor_earnings',views.instructor_earnings,name='instructor_earnings'),
    path('instructor_edit_invoice',views.instructor_edit_invoice,name='instructor_edit_invoice'),
    path('instructor_help_center',views.instructor_help_center,name='instructor_help_center'),
    path('instructor_invoice',views.instructor_invoice,name='instructor_invoice'),
    
    path('instructor_module_add/<slug:slug>',views.instructor_module_add,name='instructor_module_add'),
    path('instructor_module_edit/<slug>/<sslug>',views.instructor_module_edit,name='instructor_module_edit'),
    path('instructor_module_edit_save/<slug>',views.instructor_module_edit_save,name='instructor_module_edit_save'),
    
    path('instructor_lesson_add/<slug:slug>/<sslug>',views.instructor_lesson_add,name='instructor_lesson_add'),
    path('instructor_lesson_edit/<slug>/<sslug>/<ssslug>',views.instructor_lesson_edit,name='instructor_lesson_edit'),
    path('instructor_lesson_edit_save/<slug>/<sslug>',views.instructor_lesson_edit_save,name='instructor_lesson_edit_save'),
    
    path('instructor_course_publish/<slug:slug>',views.instructor_course_publish,name='instructor_course_publish'),
    path('check_course_session/<slug:slug>/<sslug>/<ssslug>',views.check_course_session,name='check_course_session'),
    
    
    path('instructor_messages',views.instructor_messages,name='instructor_messages'),
    path('instructor_quiz_edit',views.instructor_quiz_edit,name='instructor_quiz_edit'),
    path('instructor_quizzes',views.instructor_quizzes,name='instructor_quizzes'),
    path('instructor_review_quiz',views.instructor_review_quiz,name='instructor_review_quiz'),
    path('instructor_forum',views.instructor_forum,name='instructor_forum'),
    path('instructor_statement',views.instructor_statement,name='instructor_statement'),
    path('instructor_forum_ask',views.instructor_forum_ask,name='instructor_forum_ask'),
    path('instructor_forum_thread',views.instructor_forum_thread,name='instructor_forum_thread'),
    path('instructor_profile',views.instructor_profile,name='instructor_profile'),
    path('instructor_billing',views.instructor_billing,name='instructor_billing'),
    
    path('instructor_my_courses',views.instructor_my_courses,name='instructor_my_courses'),
    path('instructor_view_course/<slug:slug>',views.instructor_view_course,name='instructor_view_course'),
    
    path('instructor_logout',views.instructor_logout,name='instructor_logout'),
    
    path('delete_module/<slug:slug>/<sslug>',views.delete_module,name='delete_module'),
    path('delete_course/<slug:slug>',views.delete_course,name='delete_course'),
    path('delete_session/<slug>/<sslug>/<ssslug>',views.delete_session,name='delete_session'),
    
    path('in_base',views.in_base,name='in_base'),
    path('test',views.test,name='test'),
   
]
