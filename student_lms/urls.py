from django.urls import path
from .import views

urlpatterns = [
    path('', views.student_dashboard,name='student_dashboard'),
    path('student_account_edit', views.student_account_edit,name='student_account_edit'),
    path('student_account_edit_save', views.student_account_edit_save,name='student_account_edit_save'),
    path('student_account_edit_basic', views.student_account_edit_basic,name='student_account_edit_basic'),
    path('student_account_edit_profile', views.student_account_edit_profile,name='student_account_edit_profile'),
    path('student_billing', views.student_billing,name='student_billing'),
    path('student_browse_courses', views.student_browse_courses,name='student_browse_courses'),
    path('student_cart/<slug:slug>', views.student_cart,name='student_cart'),
    path('student_help_center', views.student_help_center,name='student_help_center'),
    path('student_invoice/<id>', views.student_invoice,name='student_invoice'),
    path('student_fail/<id>', views.student_fail,name='student_fail'),
    path('student_messages', views.student_messages,name='student_messages'),
    path('student_messages_2', views.student_messages_2,name='student_messages_2'),
    path('student_my_courses', views.student_my_courses,name='student_my_courses'),
    path('student_pay/<slug:slug>', views.student_pay,name='student_pay'),
    path('student_quiz_results', views.student_quiz_results,name='student_quiz_results'),
    path('student_take_course/<slug:slug>', views.student_take_course,name='student_take_course'),
    path('student_take_course_session/<course_slug>/<slug>/<sslug>', views.student_take_course_session,name='student_take_course_session'),
    path('student_take_quiz', views.student_take_quiz,name='student_take_quiz'),
    path('student_view_course', views.student_view_course,name='student_view_course'),
    path('student_account_billing_payment_information', views.student_account_billing_payment_information,name='student_account_billing_payment_information'),
    path('student_account_billing_subscription', views.student_account_billing_subscription,name='student_account_billing_subscription'),
    path('student_account_billing_upgrade', views.student_account_billing_upgrade,name='student_account_billing_upgrade'),
    path('student_forum', views.student_forum,name='student_forum'),
    path('student_forum_ask', views.student_forum_ask,name='student_forum_ask'),
    path('student_forum_thread', views.student_forum_thread,name='student_forum_thread'),
    path('sessionComment/<course_slug>/<slug>/<sslug>', views.sessionComment,name='sessionComment'),
    path('sessionComment_view/<course_slug>/<slug>/<sslug>', views.sessionComment_view,name='sessionComment_view'),
    path('student_profile', views.student_profile,name='student_profile'),
    path('student_profile_posts', views.student_profile_posts,name='student_profile_posts'),
    path('student_logout', views.student_logout,name='student_logout'),   
    path('lms_base', views.lms_base,name='lms_base'),   
    path('handlerequest', views.handlerequest,name='handlerequest'),   
    path('modules/<slug>', views.modules,name='modules'),   
    path('session/<course_slug>/<slug>', views.session,name='session'),   
    path('session_view/<course_slug>/<slug>/<sslug>', views.session_view,name='session_view'),   
    path('session_seen/<course_slug>/<slug>/<sslug>', views.session_seen,name='session_seen'),

]