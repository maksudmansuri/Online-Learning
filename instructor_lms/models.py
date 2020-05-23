from django.db import models
from django.contrib.auth.models import User
from accounts.models import Staffs
# Create your models here.

    
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# class InstructorDetail(models.Model):
#     instructor_id=models.ForeignKey(User,on_delete=models.CASCADE)
#     instructor_email=models.EmailField(max_length=254)
#     instructor=models.CharField(max_length=50,blank=True,null=True)
#     instructor_fname=models.CharField(max_length=50,blank=True,null=True)
#     instructor_lname=models.CharField(max_length=50,blank=True,null=True)
#     instructor_address=models.CharField(max_length=50,blank=True,null=True)
#     instructor_city=models.CharField(max_length=50,blank=True,null=True)
#     instructor_state=models.CharField(max_length=50,blank=True,null=True)
#     instructor_country=models.CharField(max_length=50,blank=True,null=True)
#     instructor_mobile=models.CharField(max_length=50,blank=True,null=True)
#     instructor_qualification=models.CharField(max_length=50,blank=True,null=True)
#     instructor_specialist=models.CharField(max_length=50,blank=True,null=True)
# 	#instructor_fname=models.CharField(max_length=50,blank=True,null=True)
# #	instructor_lname=models.CharField(max_length=50)
#     instructor_photo=models.ImageField(upload_to="instructor/profile", height_field=None, width_field=None, max_length=None)
#     instructor_experience=models.CharField(max_length=50,blank=True,null=True)
#     instructor_ratting=models.CharField(max_length=50,blank=True,null=True)
#     instructor_courses=models.CharField(max_length=50,blank=True,null=True)
#     instructor_working=models.CharField(max_length=50,blank=True,null=True)
#     instructor_website=models.URLField(max_length=200,blank=True,null=True)
#     instructor_linkdin=models.URLField(max_length=200,blank=True,null=True)
    
#     def __str__(self):
#         return self.fname
    



    