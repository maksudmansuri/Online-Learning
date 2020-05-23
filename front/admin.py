from django.contrib import admin
from .models import Course,CourseCategory,CourseSubCategory,Course_Session,Course_Modules

admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(CourseSubCategory)
admin.site.register(Course_Session)
admin.site.register(Course_Modules)
