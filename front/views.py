from django.shortcuts import render , redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Course,Course_Session,CourseCategory,CourseSubCategory,Course_Modules
from math import ceil
from accounts.EmailBackEnd import EmailBackEnd
from django.db.models import Q
from django.core.paginator import Page,PageNotAnInteger,Paginator
from accounts.models import Staffs, Students
# Create your vie ws here.v
 
def index(request):
    allcourse=[]
    allcats=[]
    allcrs=Course.objects.all()
    allcrscnt=Course.objects.all().count()
    allstfcnt=Staffs.objects.all().count()
    allstdcnt=Students.objects.all().count()
    catcourse=Course.objects.values('course_category','id')
    cats={item['course_category'] for item in catcourse}
    for cat in cats:
        allcat=CourseCategory.objects.get(id=cat)
        crs=Course.objects.filter(course_category=cat,is_verified=True)
        n=len(crs)
        # nSlides=n/4+ceil((n/4)-(n//4))    
        allcourse.append([crs,range(1,n)])
        allcats.append(allcat)
        for i in crs:
            print(i.course_category)
    params= {'allcourse':allcourse,'allcats':allcats,'allcrscnt':allcrscnt,'allstfcnt':allstfcnt,'allstdcnt':allstdcnt,'allcrs':allcrs}
    return render(request,'index.html',params)
    
def home_two(request):
    return render(request,'home_two.html')

def search_list(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        courses = Course.objects.filter(
            (Q(course_name__icontains = q) | Q(course_desc__icontains = q)) & Q(is_verified=True) 
            ).distinct()

        for course in courses:
            queryset.append(course)
    
    return list(set(queryset)) 

def course_list(request):
    stf=Staffs.objects.all()
    allcrs=Course.objects.all()
    courses=[]
    allcats=[]
    catcourse=Course.objects.values('course_category','id')
    cats={item['course_category'] for item in catcourse}
    for cat in cats:
        allcat=CourseCategory.objects.get(id=cat)
        # crs=Course.objects.filter(course_category=cat,is_verified=True)
        crscnt=Course.objects.filter(course_category=cat).count()
        # nSlides=n/4+ceil((n/4)-(n//4))
        # courses.append(crs)
        allcats.append([allcat,crscnt])

    courses=Course.objects.filter(is_verified=True)
    cnt=Course.objects.filter().count()
    # allcat=CourseCategory.objects.all()
    allsubcat=CourseSubCategory.objects.all()
    paginator=Paginator(courses,6)
    page=request.GET.get('page')
    courses=paginator.get_page(page)
    param={'allcat':allcats,'allsubcat':allsubcat,'courses1':courses,'cnt':cnt,'stf':stf,'allcrs':allcrs}
    return render(request,'course_list.html',param)

def testing_file(request):
    allcourse=[]
    catcourse=Course.objects.values('course_category','course_code')
    cats={item['course_category'] for item in catcourse}
    for cat in cats:
        crs=Course.objects.filter(course_category=cat)
        n=len(crs)
        nSlides=n/4+ceil((n/4)-(n//4))    
        allcourse.append([crs,range(1,n),nSlides])
    # courses=Course.objects.all()
    # print(courses)
    # n=len(courses)
    # nSlides=n/3+ceil((n/4)-(n//4))
    #  params= {'no_of_slides':n, 'range':range(0,n), 'course':courses}
    # print(params)
    params= {'allcourse':allcourse}
    print(crs)
    
    return render(request,'testing_file.html',params)

def course_details(request,slug):
    stf=Staffs.objects.all()
    allcrs=Course.objects.all()
    crs=Course.objects.get(course_slug=slug)
    crs_ssn=Course_Modules.objects.filter(course=crs)
    # crs_ssn=Course_Session.objects.filter(module.course_id==mdl.course)
    print(crs_ssn)
    crssame=Course.objects.filter(course_category=crs.course_category)
    # crssame=Course.objects.all()
    params= {'crs1':crs,'crs_ssn1':crs_ssn,'crssame1':crssame,'stf':stf,'allcrs':allcrs}
    return render(request,'course_details.html',params)

def course_details_2(request):
    return render(request,'course_details_2.html')

def dologout(request):
    logout(request)
    return redirect('/')

def instructor_logout(request):
    logout(request)
    return redirect('/login')

def about_us(request):
    stf=Staffs.objects.all()
    allcrs=Course.objects.all()
    param={'stf':stf,'allcrs':allcrs}
    return render(request,'about-us.html',param)

def career(request):
    return render(request,'career.html')

def contact_us(request):
    return render(request,'contact-us.html')