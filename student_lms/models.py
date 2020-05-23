from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Students
from front.models import Course

# Create your models here.
class Discount(models.Model):
    id=models.AutoField(primary_key=True)
    discount=models.CharField(max_length=100,null=True,blank=True)
    code=models.CharField(max_length=50,null=True,blank=True)
    percentage=models.FloatField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    expired_date=models.DateTimeField(null=True,blank=True)
    objects = models.Manager()

class Orders(models.Model):
    id=models.AutoField(primary_key=True)
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    discount=models.ForeignKey(Discount,on_delete=models.CASCADE)
    orders_date=models.DateTimeField(auto_now_add=True)
    student_phone=models.CharField(max_length=50,default=0)
    student_email=models.EmailField(max_length=254,default="")
    objects = models.Manager()

    def __str__(self):
         return self.student_name

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Ratting(models.Model):
    id=models.AutoField(primary_key=True)
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    ratting=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()    
