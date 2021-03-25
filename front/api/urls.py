from front.api import views
from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken import views as authviews


urlpatterns = [
    path('<slug>/',views.api_detail_course_view,name="detail"),
    path('module/<id>/',views.ApiCourseModuleListView.as_view(),name="moduleslist"),
    path('create',views.api_create_course_view,name="create"),
    path('<slug>/delete',views.api_delete_course_view,name="delete"),
    path('<slug>/update',views.api_update_course_view,name="update"),
    path('list',views.ApiCourseListView.as_view(),name="list"),
    path('<slug>/is_teacher',views.api_is_teacher_of_course,name="is_teacher"),

    
]