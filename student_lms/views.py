from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Course,Course_Session,Course_Modules,CourseCategory,CourseSubCategory
from .models import Orders,Ratting,paytm_payment
from accounts.models import Students,CustomUser
from front.models import viewed,SessionComments
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Page,PageNotAnInteger,Paginator
import moviepy.editor
from front.views import search_list
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
# Create your views  h ere.
MERCHANT_KEY = 'bBzG2&6OfWiZzlT0'

def student_logout(request):
    logout(request)
    return redirect('/accounts/dologin')

@login_required
def lms_base(request):
    std=Students.objects.get(admin=request.user.id)
    return render(request,'student_lms/lms_base.html',{'std1':std})
    
@login_required
def student_dashboard(request):
    std=Students.objects.get(admin=request.user)
    ordcrs=Orders.objects.filter(student=std)
    cntssns=0
    per=0
    tlssns=0
    vwdsns=0
    allinone = []
    for ord in ordcrs:
        getvwd=viewed.objects.get(course=ord.course.id)
        getcsr=Course.objects.get(id=ord.course.id)
        getml=Course_Modules.objects.get(course=getcsr,position=int(getvwd.module_position))
        getssn=Course_Session.objects.get(module=getml,position=int(getvwd.session_position))
        cntmls=Course_Modules.objects.filter(course=ord.course)
        for cntml in cntmls:
            if cntml.position < int(getvwd.module_position):
                cntssns = Course_Session.objects.filter(module=cntml).count()
                tlssns=tlssns + cntssns
                vwdsns=vwdsns + cntssns
                print(tlssns)
            elif cntml.position == int(getvwd.module_position):
                vwdssns = Course_Session.objects.filter(module=cntml)
                cntvwdssn=0
                for vwdssn in vwdssns:
                    if vwdssn.position <= int(getvwd.session_position):
                        vwdsns = vwdsns + 1
                        tlssns=tlssns + 1
                    else:
                        tlssns=tlssns + 1
            else:
                cntssns = Course_Session.objects.filter(module=cntml).count()
                tlssns=tlssns + cntssns
        per = (vwdsns * 100) / tlssns
        allinone.append([ord,getcsr,getml,getssn,per,vwdsns,tlssns])
        print(allinone)   
    param={'allinone':allinone,'std1':std}
    return render(request,'student_lms/student_dashboard.html',param)

@login_required
def student_account_edit_save(request):
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
        try:
            user=CustomUser.objects.get(id=std_id)
            user.first_name=fisrt_name
            user.last_name=last_name
            user.save() 
                
            std_model=Students.objects.get(admin=std_id)
            print(std_model)
            std_model.fisrt_name=fisrt_name
            std_model.last_name=last_name
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
        except:
            messages.success(request,"Failed To Edit:")
            return HttpResponseRedirect("/student_lms/student_account_edit")
    
@login_required
def student_account_edit(request):
    std=Students.objects.get(admin=request.user)
    print(std.dob)
    return render(request,'student_lms/student_account_edit.html',{'std1':std})
            
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
    # query = ""
    # if request.GET:
    #     query = request.GET['q']
    #     query=str(query)
    
    crs=Course.objects.filter(is_verified=True)
    paginator=Paginator(crs,6)
    page=request.GET.get('page')
    crs=paginator.get_page(page)
    return render(request,'student_lms/student_browse_courses.html',{'crs':crs,'std1':std})

@login_required()
def student_cart(request,slug):
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=slug)
    if Orders.objects.filter(course=crs.id).exists():
        messages.add_message(request,messages.ERROR,"Course already purchased")
        return render(request,'student_lms/student_cart.html',{'crs1':crs,'std1':std})
    if request.method=="POST":
        user=Students.objects.get(admin=request.user.id)
        print(std.admin)
        order=Orders(student=user,course=crs,student_phone=user.phone,student_email=user.admin.email)
        order.save()
        return redirect(f"/student_lms/student_pay/{crs.course_slug}",kwargs={'crs1': crs,'std1':std}) 
    return render(request,'student_lms/student_cart.html',{'crs1':crs,'std1':std})

@login_required() 
def student_help_center(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_help_center.html')

@login_required()
def student_fail(request):    
    return render(request,'student_lms/student_fail.html')

@login_required()
def student_invoice(request,id):
    cnf_ord=paytm_payment.objects.get(ORDERID=id)
    ord=Orders.objects.get(id=id)
    std=Students.objects.get(admin=request.user.id)
    return render(request,'student_lms/student_invoice.html',{'cnf_ord':cnf_ord,'std1':std,'ord':ord})

def student_messages(request):
    std=Students.objects.get(admin=request.user)

    return render(request,'student_lms/student_messages.html')

def student_messages_2(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'student_lms/student_messages_2.html')

@login_required()
def student_my_courses(request):
    std=Students.objects.get(admin=request.user)
    ordcrs=Orders.objects.filter(student=std)
    cntssns=0
    per=0
    tlssns=0
    vwdsns=0
    allinone = []
    for ord in ordcrs:
        getvwd=viewed.objects.get(student=std,course=ord.course.id)
        getcsr=Course.objects.get(id=ord.course.id)
        print(getcsr)
        getml=Course_Modules.objects.get(course=getcsr,position=int(getvwd.module_position))
        print(getml)
        getssn=Course_Session.objects.get(module=getml,position=int(getvwd.session_position))
        print(getssn)
        cntmls=Course_Modules.objects.filter(course=ord.course)
        for cntml in cntmls:
            if cntml.position < int(getvwd.module_position):
                cntssns = Course_Session.objects.filter(module=cntml).count()
                tlssns=tlssns + cntssns
                vwdsns=vwdsns + cntssns
            elif cntml.position == int(getvwd.module_position):
                vwdssns = Course_Session.objects.filter(module=cntml)
                cntvwdssn=0
                for vwdssn in vwdssns:
                    if vwdssn.position <= int(getvwd.session_position):
                        vwdsns = vwdsns + 1
                        tlssns=tlssns + 1
                    else:
                        tlssns=tlssns + 1
            else:
                cntssns = Course_Session.objects.filter(module=cntml).count()
                tlssns=tlssns + cntssns
        per = (vwdsns * 100) / tlssns
        allinone.append([ord,getcsr,getml,getssn,per,vwdsns,tlssns])   
    paginator=Paginator(allinone,6)
    page=request.GET.get('page')
    allinone=paginator.get_page(page)
    param={'allinone':allinone,'std1':std}      
    return render(request,'student_lms/student_my_courses.html',param)

def student_pay(request,slug):
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=slug)
    ords=Orders.objects.get(course=crs.id)
    param_dict = {
            'MID':'VCqddy35812500980656',
            'ORDER_ID':str(ords.id),
            'TXN_AMOUNT':str(5000),
            'CUST_ID':request.user.email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/student_lms/handlerequest',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request,'student_lms/paytm.html',{'param_dict':param_dict,'std1':std})

    # return render(request,'student_lms/student_pay.html',{'std1':std})

@csrf_exempt
def handlerequest(request):
    form=request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    print(response_dict)    
    CURRENCY = request.POST['CURRENCY']
    GATEWAYNAME = request.POST['GATEWAYNAME']
    RESPMSG = request.POST['RESPMSG']
    BANKNAME = request.POST['BANKNAME']
    PAYMENTMODE = request.POST['PAYMENTMODE']
    RESPCODE = request.POST['RESPCODE']
    TXNID = request.POST['TXNID']
    TXNAMOUNT = request.POST['TXNAMOUNT']
    ORDERID = request.POST['ORDERID']
    STATUS = request.POST['STATUS']
    BANKTXNID = request.POST['BANKTXNID']
    TXNDATE = request.POST['TXNDATE']
    ord_cmf=paytm_payment(CURRENCY=CURRENCY,
    GATEWAYNAME=GATEWAYNAME,
    RESPMSG=RESPMSG,
    BANKNAME=BANKNAME,
    PAYMENTMODE=PAYMENTMODE,
    RESPCODE=RESPCODE,
    TXNID=TXNID,
    TXNAMOUNT=TXNAMOUNT,
    ORDERID=ORDERID,
    STATUS=STATUS,
    BANKTXNID=BANKTXNID,
    TXNDATE=TXNDATE)
    ord_cmf.save()
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order Successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request,'student_lms/paytm_status.html',{'response':response_dict})
             
def student_quiz_results(request):
    if request.session.has_key('logged in'):
        if request.user.user_type!="3":
            messages.error(request,"Invvalid Page :")
            return redirect("/accounts/dologin")
        return render(request,'student_lms/student_quiz_results.html')
    return redirect("/accounts/dologin")

def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds

@login_required()
def session(request,course_slug,slug):
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=course_slug,)
    allml=Course_Modules.objects.filter(course=crs)
    ml=Course_Modules.objects.get(slug=slug,course=crs)
    allssn=Course_Session.objects.filter(module=ml)
    lastssn=Course_Session.objects.filter(module=ml).last()
    getvwssn=lastssn.position + 1
    crssn2=Course_Session.objects.filter(module=ml)
    param={'crs':crs,'allssn':allssn,'ssn':crssn2,'std1':std,'ml':ml,'getvwssn':getvwssn}
    return render(request,'student_lms/session.html',param)
    # return redirect("/accounts/dologin")

@login_required()
def session_seen(request,course_slug,slug,sslug):
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=course_slug)
    allml=Course_Modules.objects.filter(course=crs)
    ml=Course_Modules.objects.get(slug=slug,course=crs)
    allssn=Course_Session.objects.filter(module=ml)
    crssn2=Course_Session.objects.get(course_slug=sslug,module=ml)
    cmmnts=SessionComments.objects.filter(session=crssn2)
    param={'crs':crs,'allssn':allssn,'ssn':crssn2,'std1':std,'ml':ml,'cmmnts':cmmnts}
    return render(request,'student_lms/session_seen.html',param)

@login_required()
def session_view(request,course_slug,slug,sslug):
    std=Students.objects.get(admin=request.user)
    crs=Course.objects.get(course_slug=course_slug)
    allml=Course_Modules.objects.filter(course=crs)
    ml=Course_Modules.objects.get(slug=slug,course=crs)
    allssn=Course_Session.objects.filter(module=ml)
    lastssn=Course_Session.objects.filter(module=ml).last()
    lastml=Course_Modules.objects.filter(course=crs).last()
    crssn2=Course_Session.objects.get(course_slug=sslug,module=ml)
    cmmnts=SessionComments.objects.filter(session=crssn2)
    print(crs)
    print(std)
    print(ml)
    print(lastssn)
    print(lastml)
    print(crssn2)
    vwd1=viewed.objects.get(student=std,course=crs.id)
    print(vwd1)
    getvwssn=int(vwd1.session_position)
    getvwml=int(vwd1.module_position)
    if request.method == "POST":
        course=request.POST['ccrs']
        module=request.POST['cmdl']
        session=int(request.POST['cssn'])
        if viewed.objects.filter(student=std,course=course).exists():
            vwd=viewed.objects.get(student=std,course=course)
            this=int(vwd.session_position)
            that=int(vwd.module_position)  
            if this == getvwssn:
                if this == lastssn.position:
                    if that == lastml.position:
                        pass
                    else:
                        that = that + 1 
                        this=1
                else:
                    this=session+1
            elif this < getvwssn:
                this = session
            else:
                pass
            vwd.session_position=this
            vwd.module_position=that
            vwd.save()
            
    # getvwd=viewed.objects.filter(student=std)
    if viewed.objects.filter(student=std,course=crs.id,module_position=ml.position).exists():
        vwd=viewed.objects.get(student=std,course=crs.id,module_position=ml.position)
        getcsr=Course.objects.get(id=crs.id)
        getml=Course_Modules.objects.get(position=int(ml.position),course=getcsr)
        getssn=Course_Session.objects.get(position=int(vwd.session_position),module=getml)
        getvwssn = int(vwd.session_position)

                  
    param={'crs':crs,'allssn':allssn,'ssn':crssn2,'std1':std,'ml':ml,'getvwssn':getvwssn,'cmmnts':cmmnts,'getvwml':getvwml}
    return render(request,'student_lms/session_view.html',param)

def sessionComment_view(request,course_slug,slug,sslug):
    crs=Course.objects.get(course_slug=course_slug)
    crs=Course.objects.get(course_slug=course_slug)
    ml=Course_Modules.objects.get(slug=slug,course=crs)
    ssn=Course_Session.objects.get(module=ml,course_slug=sslug)
    if request.method=="POST":
        user = request.user
        session = ssn
        comment = request.POST.get("comment")

        cmmnt=SessionComments(user=user,session=session,comment=comment)
        cmmnt.save()
        messages.add_message(request,messages.SUCCESS,"Comment Posted Successfuly")

    return redirect(f"/student_lms/session_view/{crs.course_slug}/{ml.slug}/{ssn.course_slug}") 

def sessionComment(request,course_slug,slug,sslug):
    crs=Course.objects.get(course_slug=course_slug)
    crs=Course.objects.get(course_slug=course_slug)
    ml=Course_Modules.objects.get(slug=slug,course=crs)
    ssn=Course_Session.objects.get(module=ml,course_slug=sslug)
    if request.method=="POST":
        user = request.user
        session = ssn
        comment = request.POST.get("comment")

        cmmnt=SessionComments(user=user,session=session,comment=comment)
        cmmnt.save()
        messages.add_message(request,messages.SUCCESS,"Comment Posted Successfuly")

    return redirect(f"/student_lms/session_seen/{crs.course_slug}/{ml.slug}/{ssn.course_slug}")

@login_required() 
def modules(request,slug):
    crssn=[]
    getvwml=1
    std=Students.objects.get(admin=request.user.id)
    crs=Course.objects.get(course_slug=slug)
    mdl=Course_Modules.objects.filter(course=crs)   
    getcsr=crs
    getml=1
    getssn=1
    getvwml=1
    if viewed.objects.filter(student=std.id,course=crs.id).exists():
        getmls = viewed.objects.get(student=std,course=crs.id)
        getml=Course_Modules.objects.get(course=crs,position=int(getmls.module_position))
        getssn=Course_Session.objects.get(module=int(getmls.module_position),position=int(getmls.session_position))
        getvwml = int(getmls.module_position)
    else:
        vd=viewed(student=std,course=crs.id,module_position='1',session_position='1')
        vd.save()
        getmls = viewed.objects.get(student=std,course=crs.id)
        getml=Course_Modules.objects.get(course=crs,position=int(getmls.module_position))
        getssn=Course_Session.objects.get(module=int(getmls.module_position),position=int(getmls.session_position))
        getvwml = int(getmls.module_position)
    for ml in mdl:
        mlcrssn=Course_Session.objects.filter(module=ml)
        n=len(mlcrssn)
        crssn.append([mlcrssn,ml,n])
    param={'crs1':crs,'crssn1':crssn,'std1':std,'getvwml':getvwml,'getcsr':getcsr,'getml':getml,'getssn':getssn}
    return render(request,'student_lms/modules.html',param)

@login_required()
def student_take_course_session(request,course_slug,slug,sslug):
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

