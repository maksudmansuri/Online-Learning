from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin 
from django.urls import reverse
from django.shortcuts import redirect

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,views_func,view_args,view_kwargs):
        modulename=views_func.__module__

        user=request.user
        if user.is_authenticated:
            if user.user_type=="1":
                if modulename == "counsellor.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media.views":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("counsellor_dashboard"))
            elif user.user_type=="2":
                if modulename == "instructor_lms.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("instructor_dashboard"))
            elif user.user_type=="3":
                if modulename == "student_lms.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_dashboard"))
            # elif user.user_type=="4":
            #     if modulename == "django.contrib.admin" or modulename == "django.views.static":
            #         pass
            #     if modulename == "front.views":
            #         pass
            #     elif modulename == "media":
            #         pass
            #     # else:
            #     #     return redirect("/admin")
            #         # return HttpResponseRedirect(reverse("django/contrib/admin"))
            else:
                if modulename == "django.contrib.auth.views":
                    pass
                if modulename == "front.views":
                    pass
                return redirect('admin')
        else:
            if request.path == reverse("dologin") or modulename == "front.views" or modulename == "accounts.views" or modulename == "django.views.static" or modulename == "django.contrib.auth.views" or modulename == "chat.views" or modulename == "accounts.api.views" or modulename == "front.api.views" or request.path == reverse("login"):
                pass
            else:
                return HttpResponseRedirect(reverse("dologin"))

