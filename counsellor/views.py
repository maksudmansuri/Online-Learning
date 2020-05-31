from django.shortcuts import render,redirect
# from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Course
# from .models import Orders,StudentDetail
import logging
from accounts.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from accounts.models import Staffs,Students,CustomUser
from django.core.paginator import Page,PageNotAnInteger,Paginator
from front.models import Course,Course_Modules,Course_Session,CourseCategory,CourseSubCategory
from django.db.models import Q

def counsellor_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        #check user is authenticate or not
        user=EmailBackEnd.authenticate(request,email,password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect("/counsellor")
        else:
            messages.error(request,"Invalid Email or Password please try again:")
            return render(request,'counsellor/dologin.html')

    return render(request,'counsellor/dologin.html')

def counsellor_logout(request):
    logout(request)
    return redirect('/accounts/dologin')

def counsellor_dashboard(request):
    # if request.session.has_key('logged in'):
    #     if request.user.user_type=="1":
    return render(request,'counsellor/counsellor_dashboard.html')
    #     else:
    #         messages.error(request,"Invvalid Page :")
    #         return redirect("/accounts/dologin")

    # return redirect("/accounts/dologin")    

def manage_staff(request):
    stf=Staffs.objects.filter((Q(is_appiled=True) | Q(is_verified=True)) & Q(admin__is_active=True) &  Q(admin__user_type=2) )
    paginator=Paginator(stf,3)
    page=request.GET.get('page')
    stf=paginator.get_page(page)
    return render(request,'counsellor/manage_staff.html',{'stf':stf})
 
def staff_activate(request,id):
    stf=Staffs.objects.filter((Q(is_appiled=True) | Q(is_verified=True)) & Q(admin__is_active=True) &  Q(admin__user_type=2))
    astf=Staffs.objects.get(admin_id=id)
    if astf is not None and astf.is_verified == False and astf.is_appiled == True:
        astf.is_verified=True
        astf.save()
    # stf=Staffs.objects.all()
    paginator=Paginator(stf,3)
    page=request.GET.get('page')
    stf=paginator.get_page(page)
    return render(request,'counsellor/manage_staff.html',{'stf':stf})

def staff_deactivate(request,id):
    astf=Staffs.objects.get(admin_id=id)
    if astf is not None and astf.is_verified == True:
        astf.is_verified=False
        astf.is_appiled=False
        astf.save()
    stf=Staffs.objects.filter((Q(is_appiled=True) | Q(is_verified=True)) & Q(admin__is_active=True) &  Q(admin__user_type=2))
    paginator=Paginator(stf,3)
    page=request.GET.get('page')
    stf=paginator.get_page(page)
    return render(request,'counsellor/manage_staff.html',{'stf':stf})

def manage_student(request):
    std=Students.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    paginator=Paginator(std,3)
    page=request.GET.get('page')
    std=paginator.get_page(page)
    return render(request,'counsellor/manage_student.html',{'std':std})

def student_activate(request,id):
    astd=Students.objects.get(admin_id=id)
    if astd is not None and astd.is_verified == False:
        astd.is_verified=True
        astd.save()
    std=Students.objects.filter((Q(is_appiled=True) | Q(is_verified=True)) & Q(admin__is_active=True) &  Q(admin__user_type=3))
    paginator=Paginator(std,3)
    page=request.GET.get('page')
    std=paginator.get_page(page)
    return render(request,'counsellor/manage_student.html',{'std':std})

def student_deactivate(request,id):
    astd=Students.objects.get(admin_id=id)
    if astd is not None and astd.is_verified == True:
        astd.is_verified=False
        astd.is_appiled=True
        astd.save()
    std=Students.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    paginator=Paginator(std,3)
    page=request.GET.get('page')
    std=paginator.get_page(page)
    return render(request,'counsellor/manage_student.html',{'std':std})

def course_category(request):
    if request.method == "POST":
        category=request.POST['category']
        cat=CourseCategory(category=category)
        cat.save()
    crscats=CourseCategory.objects.all()
    return render(request,'counsellor/course_category.html',{'crscats':crscats}) 

def course_category_delete(request,id):
    detcrscats=CourseCategory.objects.get(id=id).delete()
    crscats=CourseCategory.objects.all()
    return render(request,'counsellor/course_category.html',{'crscats':crscats}) 

def course_subcategory(request,id):
    crscats=CourseCategory.objects.get(id=id)
    if request.method == "POST":
        category=crscats
        subcategory=request.POST['subcategory']
        cat=CourseSubCategory(category=category,subcategory=subcategory)
        cat.save()
    crssbcats=CourseSubCategory.objects.filter(category=crscats.id)
    return render(request,'counsellor/course_subcategory.html',{'crssbcats':crssbcats,'crscats':crscats}) 

def course_subcategory_delete(request,sid,id):
    crscats=CourseCategory.objects.get(id=sid)
    detcrssbcats=CourseSubCategory.objects.get(id=id).delete()
    crssbcats=CourseSubCategory.objects.filter(category=crscats.id)
    return render(request,'counsellor/course_subcategory.html',{'crssbcats':crssbcats,'crscats':crscats}) 

def manage_course(request):
    allcrs=Course.objects.filter(Q(is_appiled =True) | Q(is_verified=True))
    allcnt=[]
    for crs in allcrs: 
        cnt=0
        mdl=Course_Modules.objects.filter(course=crs)
        for ml in mdl:
            mlcrssn=Course_Session.objects.filter(module=ml)
            for i in mlcrssn:
                if i.is_verified != True:
                    i.is_appiled=True
                    i.save()
                    cnt=cnt+1
        allcnt.append([cnt,crs])
    print(allcnt)
    # allcrs=Course.objects.all( )
    paginator=Paginator(allcnt,3)
    page=request.GET.get('page')
    allcnt=paginator.get_page(page)
    return render(request,'counsellor/manage_course.html',{'crs1':allcnt})

def course_activate(request,slug):
    crs=Course.objects.get(course_slug=slug)
    allcnt=[]
    cnt1=0
    mdl=Course_Modules.objects.filter(course=crs)
    for ml in mdl:
        mlcrssn=Course_Session.objects.filter(module=ml)
        for i in mlcrssn:
            if i.is_verified != True and i.is_appiled == True:
                cnt1=cnt1+1
    print(cnt1)
    if cnt1 == 0 and crs.is_appiled == True:
        crs.is_verified = True
        crs.is_appiled = False
        crs.save()

    allcrs=Course.objects.all()
    allcnt=[]
    for crs in allcrs: 
        cnt=0
        mdl=Course_Modules.objects.filter(course=crs)
        for ml in mdl:
            mlcrssn=Course_Session.objects.filter(module=ml)
            for i in mlcrssn:
                if i.is_verified != True and i.is_appiled == True:
                    cnt=cnt+1
        allcnt.append([cnt,crs])
    paginator=Paginator(allcnt,3)
    page=request.GET.get('page')
    allcnt=paginator.get_page(page)
    return render(request,'counsellor/manage_course.html',{'crs1':allcnt})

def course_deactivate(request,slug):
    crs=Course.objects.get(course_slug=slug)
    mdl=Course_Modules.objects.filter(course=crs)
    if crs.is_verified == True and crs.is_appiled == False:
        crs.is_verified = False
        crs.is_appiled = True
        crs.save()

    allcrs=Course.objects.all()
    allcnt=[]
    for crs in allcrs: 
        cnt=0
        mdl=Course_Modules.objects.filter(course=crs)
        for ml in mdl:
            mlcrssn=Course_Session.objects.filter(module=ml)
            for i in mlcrssn:
                if i.is_verified != True and i.is_appiled == True:
                    cnt=cnt+1
        allcnt.append([cnt,crs])
    paginator=Paginator(allcnt,3)
    page=request.GET.get('page')
    allcnt=paginator.get_page(page)
    return render(request,'counsellor/manage_course.html',{'crs1':allcnt})

def check_course_session_activate(request,slug,sslug,ssslug):
    acrs=Course.objects.get(course_slug=slug)
    amdl=Course_Modules.objects.get(slug=sslug,course=acrs)
    acrssn=Course_Session.objects.get(course_slug=ssslug,module=amdl)
    print(acrssn)
    crssn=[]
    if acrssn != None: 
        if acrssn.is_verified == False and acrssn.is_appiled == True:
            acrssn.is_verified=True
            acrssn.is_appiled=False
            acrssn.save()
            print(acrssn.is_verified)
    mdl=Course_Modules.objects.filter(course=acrs)
    for ml in mdl:
        mlcrssn=Course_Session.objects.filter(module=ml)
        crssn.append([mlcrssn,ml])
        # print(crssn[0].is_verified)
    # crs=Course.objects.all()
    # paginator=Paginator(crs,3)
    # page=request.GET.get('page')
    # crs=paginator.get_page(page) 
    param={'crs1':acrs,'crssn1':crssn,'crssn2':acrssn}
    return render(request,'counsellor/check_course_session.html',param)

def check_course_session_deactivate(request,slug,sslug,ssslug):
    acrs=Course.objects.get(course_slug=slug)
    amdl=Course_Modules.objects.get(slug=sslug,course=acrs)
    acrssn=Course_Session.objects.get(course_slug=ssslug,module=amdl)
    print(acrssn)
    crssn=[]
    if acrssn != None: 
        if acrssn.is_verified == True and acrssn.is_appiled == False:
            acrssn.is_verified=False
            acrssn.is_appiled=False
            acrssn.save()
            print(acrssn.is_verified)
    mdl=Course_Modules.objects.filter(course=acrs)
    for ml in mdl:
        mlcrssn=Course_Session.objects.filter(module=ml)
        crssn.append([mlcrssn,ml])
        # print(crssn[0].is_verified)
    # crs=Course.objects.all()
    # paginator=Paginator(crs,3)
    # page=request.GET.get('page')
    # crs=paginator.get_page(page) 
    param={'crs1':acrs,'crssn1':crssn,'crssn2':acrssn}
    return render(request,'counsellor/check_course_session.html',param)

def check_course_details(request,slug):
    param=[]
    crssn=[]
    # std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=slug)
    print(crs)
    mdl=Course_Modules.objects.filter(course=crs)
    print(mdl)
    for ml in mdl:
        print(ml)
        mlcrssn=Course_Session.objects.filter(Q(module=ml) & (Q(is_appiled=True) | Q(is_verified=True)))
        print(mlcrssn)
        crssn.append([mlcrssn,ml])
    print(crssn)
    param={'crs1':crs,'crssn1':crssn}
    return render(request,'counsellor/check_course_details.html',param)

def check_course_session(request,slug,sslug,ssslug):
    # std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=slug)
    allml=Course_Modules.objects.filter(course=crs)
    ml=Course_Modules.objects.get(slug=sslug,course=crs)
    crssn2=Course_Session.objects.get(course_slug=ssslug,module=ml)
    crssn=[]        
    allml=Course_Modules.objects.filter(course=crs)
    
    for ml in allml:
        mlcrssn=Course_Session.objects.filter(module=ml)
        n=len(mlcrssn)
        crssn.append([mlcrssn,ml])
    
    param={'crs1':crs,'crssn1':crssn,'crssn2':crssn2}
    return render(request,'counsellor/check_course_session.html',param)

def add_staff(request):
    # if request.user.is_anonymous:
    #    return redirect("/accounts/dologin")
    #std_d=StudentDetail.objects.filter(username=request.user)
    # print(std_d)
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        fisrt_name=request.POST['fisrt_name']
        last_name=request.POST['last_name']
        account1=StudentDetail(username=username,student_email=student_email,password=password,fisrt_name=fisrt_name,last_name=last_name,student_qualification=student_qualification,student_dob=student_dob,student_phone=student_phone,student_photo=student_photo,student_address=student_address,student_city=student_city,student_state=student_state,student_country=student_country)
        account1.save()

def user_count(user_data):
    users=user_data
    cnt=0
    for user in users:
        if user.is_varified == True:
            cnt=cnt+1
    return cnt