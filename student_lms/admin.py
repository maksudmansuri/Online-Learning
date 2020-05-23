from django.contrib import admin
from .models import Orders,Students,Attendance,AttendanceReport,NotificationStudent,FeedBackStudent,LeaveReportStudent,Ratting
# Register your models here.

admin.site.register(Orders)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(NotificationStudent)
admin.site.register(FeedBackStudent)
admin.site.register(LeaveReportStudent)
admin.site.register(Ratting)