from django.shortcuts import render , redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Course,Course_Session,CourseCategory,CourseSubCategory,Course_Modules
from math import ceil
from accounts.EmailBackEnd import EmailBackEnd
from django.core.paginator import Page,PageNotAnInteger,Paginator
# Create your vie ws here.v


def index(request):
    allcourse=[]
    allcats=[]
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
    params= {'allcourse':allcourse,'allcats':allcats}
    return render(request,'index.html',params)
    
def home_two(request):
    return render(request,'home_two.html')

def course_list(request):
    # allcourse=[]
    courses=Course.objects.all()
    allcat=CourseCategory.objects.all()
    allsubcat=CourseSubCategory.objects.all()
    paginator=Paginator(courses,3)
    page=request.GET.get('page')
    courses=paginator.get_page(page)
    param={'allcat':allcat,'allsubcat':allsubcat,'courses1':courses}
    return render(request,'course_list.html',param)

def search_list(request):
    pass

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
    crs=Course.objects.get(course_slug=slug)
    crs_ssn=Course_Modules.objects.filter(course=crs)
    # crs_ssn=Course_Session.objects.filter(module.course_id==mdl.course)
    print(crs_ssn)
    crssame=Course.objects.filter(course_category=crs.course_category)
    # crssame=Course.objects.all()
    params= {'crs1':crs,'crs_ssn1':crs_ssn,'crssame1':crssame}
    return render(request,'course_details.html',params)

def course_details_2(request):
    return render(request,'course_details_2.html')

def dologout(request):
    logout(request)
    return redirect('/')

def instructor_logout(request):
    logout(request)
    return redirect('/login')