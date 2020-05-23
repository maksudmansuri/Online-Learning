from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Course,Course_Session,Course_Modules,CourseCategory,CourseSubCategory
from .models import Orders,Ratting
from accounts.models import Students,CustomUser
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Page,PageNotAnInteger,Paginator
# Create your views  h ere.


def student_logout(request):
    logout(request)
    return redirect('/accounts/dologin')

@login_required
def lms_base(request):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        std=Students.objects.get(admin=request.user.id)
        return render(request,'student_lms/lms_base.html',{'std1':std})
    return redirect("/accounts/dologin")

@login_required
def student_dashboard(request):
    # if request.session.has_key('logged in'):
    #     if request.user.user_type!="3":
    #         messages.error(request,"Invvalid Page :")
    #         return redirect("/accounts/dologin")
    std=Students.objects.get(admin=request.user.id)
    return render(request,'student_lms/student_dashboard.html',{'std1':std})
    #   return redirect("/accounts/dologin")

@login_required
def student_account_edit_save(request):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        else: 
            if request.method == "POST":
                std_id=request.POST['std_id']
                fisrt_name=request.POST['fisrt_name']
                last_name=request.POST['last_name']
                address=request.POST['student_address']
                city=request.POST['student_city']
                state=request.POST['student_state']
                country=request.POST['student_country']
                qualification=request.POST['student_qualification']
                dob=request.POST['student_dob']
                phone=request.POST['student_phone']
                gender=request.POST['gender']

                if request.FILES.get('photo'):
                    photo=request.FILES['photo']
                    fs=FileSystemStorage()
                    filename=fs.save(photo.name,photo)
                    photo_url=fs.url(filename)
                else:
                    photo_url=None

                user=CustomUser.objects.get(id=std_id)
                user.first_name=fisrt_name
                user.last_name=last_name
                user.save() 
               
                std_model=Students.objects.get(admin=std_id)
                print(std_model)
                std_model.address=address
                std_model.city=city
                std_model.state=state
                std_model.country=country
                std_model.qualification=qualification
                std_model.dob=dob
                std_model.phone=phone
                if photo_url!=None:
                    std_model.photo=photo_url
                    print(std_model)
                std_model.gender=gender
                std_model.is_appiled=True
                std_model.is_verified=False
                std_model.save()

                messages.success(request,"successfully Edited:")
                return HttpResponseRedirect("/student_lms/student_account_edit")
                messages.success(request,"Failed To Edit:")
                return HttpResponseRedirect("/student_lms/student_account_edit")
    return redirect("/accounts/dologin")

@login_required
def student_account_edit(request):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        else:
            std=Students.objects.get(admin=request.user)
            print(std.dob)
            return render(request,'student_lms/student_account_edit.html',{'std1':std})
    return redirect("/accounts/dologin")
        
def student_account_edit_basic(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_account_edit_basic.html')

def student_account_edit_profile(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    std=Students.objects.get(admin=request.user.id)
    return render(request,'student_lms/student_account_edit_profile.html',{'std1':std})

def student_billing(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_billing.html')

@login_required
def student_browse_courses(request):
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.filter(is_verified=True)
    return render(request,'student_lms/student_browse_courses.html',{'crs':crs,'std1':std})

@login_required() 
def student_cart(request,slug):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        std=Students.objects.get(admin=request.user.id)
        crs=Course.objects.get(course_slug=slug)
        if request.method=="POST":
            user=Students.objects.get(admin=request.user.id)
            print(user)
            order=Orders(student_name=request.user, course=crs,student_phone=user.phone,student_email=user.admin.email)
            order.save()
            return redirect("/student_lms/student_pay",kwargs={'crs1': crs,'std1':std}) 
        return render(request,'student_lms/student_cart.html',{'crs1':crs,'std1':std})
    return redirect("/accounts/dologin") 

@login_required() 
def student_help_center(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_help_center.html')

@login_required()
def student_invoice(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_invoice.html')

def student_messages(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_messages.html')

def student_messages_2(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_messages_2.html')

@login_required()
def student_my_courses(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    std=Students.objects.get(admin=request.user.id)
    ord=Orders.objects.filter(student=std)
    paginator=Paginator(ord,2)
    page=request.GET.get('page')
    ord=paginator.get_page(page)           
    return render(request,'student_lms/student_my_courses.html',{'ord1':ord,'std1':std})

@login_required()
def student_pay(request):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        else:
            std=Students.objects.get(admin=request.user.id)
            return render(request,'student_lms/student_pay.html',{'std1':std})
    else:
        return redirect("/accounts/dologin")


def student_quiz_results(request):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        return render(request,'student_lms/student_quiz_results.html')
    return redirect("/accounts/dologin")

@login_required()
def student_take_course_session(request,course_slug,slug,sslug):
    # if request.session.has_key('logged in'):
    #     if request.user.user_type!="3":
    #         messages.error(request,"Invvalid Page :")
    #         return redirect("/accounts/dologin")
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=course_slug)
    allml=Course_Modules.objects.filter(course=crs)
    ml=Course_Modules.objects.get(slug=slug,course=crs)
    crssn2=Course_Session.objects.get(course_slug=sslug,module=ml)
    crssn=[]        
    allml=Course_Modules.objects.filter(course=crs)
    for ml in allml:
        mlcrssn=Course_Session.objects.filter(module=ml)
        n=len(mlcrssn)
        crssn.append([mlcrssn,ml])

    param={'crs1':crs,'crssn1':crssn,'crssn2':crssn2,'std1':std}
    return render(request,'student_lms/student_take_course_session.html',param)
    # return redirect("/accounts/dologin")

@login_required()
def student_take_course_session_view(request,slug,sslug):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        std=Students.objects.get(admin=request.user.id)
        crs=Course.objects.filter(course_slug=course_slug)
        crssn=Course_Session.objects.filter(course_id=crs[0])
        crssn2=Course_Session.objects.get(course_slug=slug)
        param={'crs1':crs[0],'crssn1':crssn,'crssn2':crssn2,'std1':std}
        return render(request,'student_lms/student_take_course_session.html',param)
    return redirect("/accounts/dologin")

@login_required() 
def student_take_course(request,slug):
    crssn=[]
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=slug)
    mdl=Course_Modules.objects.filter(course=crs)
    for ml in mdl:
        mlcrssn=Course_Session.objects.filter(module=ml)
        n=len(mlcrssn)
        crssn.append([mlcrssn,ml])
        print(crssn)
    param={'crs1':crs,'crssn1':crssn,'std1':std}
    return render(request,'student_lms/student_take_course.html',param)

def student_take_quiz(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_take_quiz.html')

def student_view_course(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_view_course.html')

def student_account_billing_payment_information(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_account_billing_payment_information.html')

def student_account_billing_subscription(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_account_billing_subscription.html')

def student_account_billing_upgrade(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_account_billing_upgrade.html')

def student_forum(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_forum.html')

def student_forum_ask(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_forum_ask.html')

def student_forum_thread(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_forum_thread.html')

def student_profile(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_profile.html')

def student_profile_posts(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_profile_posts.html')