from django.db import models
from django.contrib.auth import user_logged_in
from ckeditor_uploader.fields import RichTextUploadingField
from instructor_lms.models import Staffs
from accounts.models import Students
from django.urls import reverse
from django.shortcuts import redirect


# Create your models  .

class CourseCategory(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.CharField(unique=True,max_length=250)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.category

class CourseSubCategory(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    subcategory=models.CharField(unique=True,max_length=250)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.subcategory  
 
class Course(models.Model):
    id=models.AutoField(primary_key=True)
    course_category=models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course_name=models.CharField(unique=True,max_length=150,blank=True,null=True)
    course_subcategory=models.ForeignKey(CourseSubCategory,on_delete=models.CASCADE)
    course_fee=models.IntegerField(blank=True,null=True)
    teacher=models.ForeignKey(Staffs ,on_delete=models.CASCADE,blank=True,null=True)
    course_duration=models.CharField(max_length=250,blank=True,null=True)
    course_image=models.ImageField(upload_to="front/images", height_field=None, width_field=None, max_length=None,blank=True,null=True)
    course_video=models.FileField(upload_to='instructor/module/session',null=True,blank=True,verbose_name="", default="")
    course_requirement=RichTextUploadingField(blank=True,null=True) 
    course_level=models.CharField(max_length=150,blank=True,null=True)
    course_desc=RichTextUploadingField(blank=True,null=True)
    course_slug=models.CharField(max_length=150,blank=True,null=True)
    course_why_take=RichTextUploadingField(blank=True,null=True)
    is_appiled=models.BooleanField(blank=True,null=True,default=False)
    is_verified=models.BooleanField(blank=True,null=True,default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
 

    def __str__(self):
        return self.course_name
   
    def get_absolute_url(self):
        return redirect('instructor_lesson_add', kwargs={'slug': self.course_slug})

class Course_Modules(models.Model):
    id=models.AutoField(primary_key=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    module=models.CharField(max_length=500,blank=True,null=True)
    module_desc=models.TextField(blank=True,null=True)
    slug=models.SlugField(blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    position=models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return self.module

class Course_Session(models.Model):
    id=models.AutoField(primary_key=True)
    module=models.ForeignKey(Course_Modules,on_delete=models.CASCADE)
    session_name=models.CharField(max_length=2150,blank=True,null=True)
    session_desc=models.TextField(blank=True,null=True)
    is_appiled=models.BooleanField(blank=True,null=True,default=False)
    is_verified=models.BooleanField(blank=True,null=True,default=False)
    session_duration=models.CharField(max_length=50,blank=True,null=True)
    course_in_pdf=models.FileField(upload_to="Course_Session/Docs", max_length=100,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    video_link=models.FileField(max_length=2000, upload_to='instructor/module/session',null=True,blank=True,verbose_name="", default="")
    course_slug=models.CharField(max_length=250,default="",blank=True,null=True)
    position=models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return self.module.module + self.session_name


class viewed(models.Model):
    id=models.AutoField(primary_key=True)
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    course=models.CharField(max_length=50,blank=True,null=True)
    module_position=models.CharField(max_length=50,blank=True,null=True)
    session_position=models.CharField(max_length=50,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    objects = models.Manager()

    def __str__(self):
        return self.student.fisrt_name + self.course.course_name
    