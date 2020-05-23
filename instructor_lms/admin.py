from django.contrib import admin
from .models import Staffs,LeaveReportStaff,FeedBackStaffs,NotificationStaffs
# Register your models here.

admin.site.register(Staffs)
admin.site.register(FeedBackStaffs)
admin.site.register(LeaveReportStaff)
admin.site.register(NotificationStaffs)
