from django.urls import path
from .import views

urlpatterns = [
    path('dologin', views.dologin,name='dologin'),
    path('instructor_singup', views.instructor_singup,name='instructor_singup'),
    path('student_singup', views.student_singup,name='student_singup'),
    path('counsellor_singup', views.counsellor_singup,name='counsellor_singup'),
    path('selection', views.selection,name='selection'),
    path('selection', views.selection,name='selection'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),

]