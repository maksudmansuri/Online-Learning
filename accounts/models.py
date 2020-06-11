from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=250,default="",null=True)
    last_name=models.CharField(max_length=250,default="",null=True)
    dob=models.DateField(blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    mobile=models.CharField(max_length=50,blank=True,null=True)
    qualification=models.CharField(max_length=50,blank=True,null=True)
    specialist=models.CharField(max_length=50,blank=True,null=True)
    instructor_photo=models.FileField(upload_to="instructor/profile",null=True)
    about=RichTextUploadingField(blank=True,null=True)
    is_appiled=models.NullBooleanField(blank=True,null=True,default=False)
    is_verified=models.NullBooleanField(blank=True,null=True,default=False)
    resume=models.FileField(upload_to="instructor/resume", max_length=250,blank=True,null=True)
    experience=models.CharField(max_length=50,blank=True,null=True)
    working_with=models.CharField(max_length=50,blank=True,null=True)
    website=models.URLField(max_length=200,blank=True,null=True)
    linkdin=models.URLField(max_length=200,blank=True,null=True)
    gender=models.CharField(max_length=200,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    objects=models.Manager()
    
    def __str__(self):
        return self.first_name  

class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    fisrt_name=models.CharField(max_length=250,blank=True,null=True)
    last_name=models.CharField(max_length=250,blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    city=models.CharField(max_length=250,blank=True,null=True)
    state=models.CharField(max_length=250,blank=True,null=True)
    country=models.CharField(max_length=250,blank=True,null=True)
    qualification =models.CharField(max_length=250,blank=True,null=True)
    dob=models.DateField(blank=True,null=True)
    phone=models.CharField(max_length=250,blank=True,null=True)
    photo=models.FileField(upload_to="student_lms/profile/images",blank=True,null=True)
    gender=models.CharField(max_length=255,null=True)
    is_appiled=models.NullBooleanField(blank=True,null=True,default=False)
    is_verified=models.NullBooleanField(blank=True,null=True,default=False)
    session_start=models.DateField(null=True)
    session_end=models.DateField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
 
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            Students.objects.create(admin=instance)
            # Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()