#############################################################
###########          Ship Easy                    ###########
###########          Project: ship easy           ###########
#############################################################
#  Program name: view.py
#  Auther: Vinie
#  Date: 24 - June - 2017
#  Time: 10:20 PM
#  M/V/C: files contain logic Create New User and basic .
#############################################################
#############################################################
import string

from django.shortcuts import render
import os

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
import random

from django.core.mail import EmailMessage


from .models import Add_user, Password_reset
from truck.models import Truck_data
from driver.models import Driver_add
from  gps.models import Aproved_mobile_number

# Create your views here.
@login_required
def index(request):
    return HttpResponse("hi Gaurav")

def register(request):
    return render(request,'signup.html')

def registration_process(request):
    transport_company_name = request.POST.get('company_name')
    user_name = request.POST.get('user_name')
    mobile_number = request.POST.get('mobile')
    email_id = request.POST.get('email')
    password = request.POST.get('pass')
    new_user = User.objects.create_user(username = user_name, password = password, email = email_id , is_active = False)
    print(new_user.id)
    subject = "testing"
    message = "Please Click on link to activate your account:http://127.0.0.1:8000/base/activete_user/"+str(new_user.id)
    email = EmailMessage(subject, message, "support@shipeasy.in", [email_id])  # emp_id['email]
    email.send()
    new_user_add = Add_user.objects.create(user_name = new_user, company_name = transport_company_name,
                                           mobile_number = mobile_number, email = email_id)
    return HttpResponse("Please Check Your Email To activation")

###### After click on url which is send on mail the user will be active


def activete_user(request,id):
    print(id)
    user_obj = User.objects.get(id = id)
    user_obj.is_active = True
    user_obj.save()
    return HttpResponseRedirect('/base/login/')


def login(request):
    login_status = (request.GET.get('status'))
    if login_status == "unsuccessful":
        error_message = "Invalid Login Or Inactive User"
    else:
        error_message = ""
    return render(request,'login.html',{'message':error_message})


def login_process(request):
    user_email = request.POST.get('email')
    user_password = request.POST.get('pwd')
    try:
        user_obj = User.objects.get(email = user_email)
    except ObjectDoesNotExist:
        user_obj = None
    print("-----------", user_obj)
    if user_obj != None:
        user = authenticate(username = user_obj.username, password = user_password)
        print("------------",user)
        if user:
            if user.is_active:
                request.session['user'] = str(user)
                return HttpResponseRedirect('/base/profile')

            else:
                print("not Active")
                return HttpResponseRedirect('/base/login/?status=unsuccessful')
        else:
            print("not a user")
            return HttpResponseRedirect('/base/login/?status=unsuccessful')
    else:
        print("Not Yet Registered")
    return HttpResponseRedirect('/base/login/?status=unsuccessful')

    # return render(request,'home.html',{'user': request.session.get('user')})

@login_required
def base(request):
    new_list = profile_for_all(request)
    return render(request, 'home.html', {'user': request.session.get('user')})


def profile(request):
    user = request.session.get('user')
    user_obj = User.objects.get(username = user)
    add_user_obj = Add_user.objects.get(user_name= user_obj.id)
    number_of_trucks = Truck_data.objects.all().count()
    number_of_driver = Driver_add.objects.all().count()
    number_of_gps_tack = Aproved_mobile_number.objects.all().count()

    # image_name = str(add_user_obj.company_logo)
    # logo =os.listdir(settings.MEDIA_ROOT+'/company_pics/')
    # print(image_name)
    # x = (image_name.split('_',1))
    # new_image = x[1]
    # new_list = []
    # print("/////////",(str(add_user_obj.user_name_id)+'_'+'c_logo'+str(new_image)))
    # for items in logo:
    #     if items.startswith(str(add_user_obj.user_name_id)+'_'+'c_logo'+"_"+new_image):
    #         new_list.append({'link': '/media/company_pics/' + items})
    #         print("////////",new_list)


    new_list = profile_for_all(request)



    # new_list = []
    # for item in logo:
    #     print("========in for")
    #     if item.startswith(str(add_user_obj.company_name) + '_'):
    #         print("in if")
    #         name = item.split('_', 1)
    #         print("name-------------",name)
    #         name = name[1]
    #         print("name-------------", name)
    #         new_list.append({'link': '/media/company_pics/' + item, 'name': name})
    #         print("=======#",new_list)

    status = (request.GET.get('status'))
    if status == "added":
        message = "Truck Added Suceess fully"
    elif status == "edited":
        message = "Driver Info Edited"

    else:
        message = ""
    return render(request, 'base/profile.html', {'user':user, 'user_obj':add_user_obj,'new_list':new_list, 'message':message,
                                                 'new_list': new_list, "truck_count":number_of_trucks,
                                                 "driver_count":number_of_driver, "no_of_gps":number_of_gps_tack})

def edit_profile_one(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    user_obj = User.objects.get(username = user)
    add_user_obj = Add_user.objects.get(user_name= user_obj.id)
    print("---------",add_user_obj.company_name)
    print("------------",user_obj)
    return render(request, 'base/edit_profile_one.html' , {"user": user, 'company_name':add_user_obj.company_name,
                                                           'user_name':user, 'new_list':new_list})


def edit_profile_one_process(request):
    user_session_id = request.session.get('user')
    user_obj = User.objects.get(username = user_session_id)
    add_user_obj = Add_user.objects.get(user_name = user_obj.id)
    if request.method == "POST":
        username = request.POST.get('username')
        company_name = request.POST.get('company_name')

        files1 = request.FILES.get('file')
        files2 = request.FILES.get('file2')
        filename1 = files1._get_name()
        database_file1 = str(user_obj.id)+"_"+filename1
        print("@@@@@@@@@@@@@@@@@@@",database_file1)
        print("----------------",filename1)
        filename2 = files2._get_name()
        database_file2 = str(user_obj.id)+"_"+filename2
        print("@@@@@@@@@@@@@@@@@@@",database_file2)

        print("----------------", filename2)
        filename1= filename1.replace(' ','_')
        filename2 = filename2.replace(' ','_')
        fd1 = open('%s/%s' % (settings.MEDIA_ROOT+'/company_pics/',str(user_obj.id)+ '_'+ 'c_logo'+ '_'+str(filename1)), 'wb')
        fd2 = open('%s/%s' % (settings.MEDIA_ROOT+'/company_pics/',str(user_obj.id)+ '_'+ 'pan'+ '_'+str(filename2)), 'wb')
        add_user_obj.company_name = company_name
        user_obj.user_name = username
        add_user_obj.company_logo = database_file1
        add_user_obj.pan_card = database_file2

        add_user_obj.save()

        for chunk in files1.chunks():
            fd1.write(chunk)
        fd1.close()
        for chunk in files2.chunks():
            fd2.write(chunk)
        fd2.close()
    return HttpResponseRedirect("/base/edit_profile_two/")

def edit_profile_two(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    user_obj = User.objects.get(username = user)
    add_user_obj = Add_user.objects.get(user_name= user_obj.id)
    print("---------",add_user_obj.company_name)
    print("------------",user_obj)
    return render(request, 'base/edit_profile_two.html', {"user": user, 'company_name':add_user_obj.company_name,
                                                           'user_name':user, 'new_list':new_list})


def edit_profile_two_process(request):
    print("in user_edit")
    print("in edit 3")
    user_session_id = request.session.get('user')
    new_list = profile_for_all(request)
    user_obj = User.objects.get(username = user_session_id)
    add_user_obj = Add_user.objects.get(user_name = user_obj.id)

    address = request.POST.get('address')
    landline = request.POST.get('landline')
    print("###########",address)
    add_user_obj.address = address
    add_user_obj.landline_number = landline
    add_user_obj.save()

    return HttpResponseRedirect("/base/edit_profile_three/")

def edit_profile_three(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    user_obj = User.objects.get(username = user)
    add_user_obj = Add_user.objects.get(user_name= user_obj.id)
    print("---------",add_user_obj.company_name)
    print("------------",user_obj)
    return render(request, 'base/edit_profile_three.html', {"user": user, 'company_name':add_user_obj.company_name,
                                                           'user_obj':add_user_obj, 'new_list':new_list})


def edit_profile_three_process(request):

    user = request.session.get('user')
    user_obj = User.objects.get(username = user)
    add_user_obj = Add_user.objects.get(user_name= user_obj.id)

    add_user_obj.contact_name = request.POST.get('owener_name')
    add_user_obj.designation = request.POST.get('designation')
    add_user_obj.mobile_number = request.POST.get('mobile_number')
    add_user_obj.email = request.POST.get('email')
    add_user_obj.save()
    return HttpResponseRedirect("/base/profile/?status=edited")


def profile_for_all(request):
    user = request.session.get('user')
    user_obj = User.objects.get(username = user)
    add_user_obj = Add_user.objects.get(user_name= user_obj.id)

    image_name = str(add_user_obj.company_logo)
    print("profile_image_pic",image_name)
    logo =os.listdir(settings.MEDIA_ROOT+'/company_pics/')
    print(image_name)
    x = (image_name.split('_',1))
    new_image = x[1]
    new_list = []
    print("/////////",(str(add_user_obj.user_name_id)+'_'+'c_logo'+str(new_image)))
    for items in logo:
        if items.startswith(str(add_user_obj.user_name_id)+'_'+'c_logo'+"_"+new_image):
            new_list.append({'link': '/media/company_pics/' + items})
            print("////////",new_list)

    return new_list


def password_reset(request):
    return render(request,'password_reset.html')


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def password_reset_process(request):
    email_user = request.POST.get('email')
    randam_key = id_generator()
    try:
        user_obj = User.objects.get(email = email_user)
        print(user_obj)
    except ObjectDoesNotExist:
        user_obj = None

    if user_obj != None:
        print(user_obj.id)
        add_user_obj = Add_user.objects.get(user_name_id= user_obj.id)

        pass_obj = Password_reset.objects.create(emil = email_user, mobile_number = str(add_user_obj.mobile_number),
                                                 otp = randam_key)
        subject = "TopTime transaction"
        messages = "Your OTP is:" + str(pass_obj.otp)
        email = EmailMessage(subject, messages, "gauravbole2@gmail.com", [email_user])  # emp_id['email]
        email.send()

        return HttpResponseRedirect('/base/otp/?email='+email_user)
    else:
        return HttpResponseRedirect('/base/reset_password')


def otp(request):
    email = request.GET.get('email')
    print("--------", email)
    return render(request,'otp_check.html',{"email":email})


def otp_check(request):
    otp = request.POST.get("otp")
    email = request.POST.get("email")
    otp_obj = Password_reset.objects.get(email = email)
    user_obj = User.objects.get(email = email)
    if otp == str(otp_obj.otp):
        return HttpResponseRedirect("base/change_password/?email"+email)
    else:
        return HttpResponseRedirect("base/otp/")


def change_password(request):
    email = request.GET.get('email')
    return render(request,'change_password.html', {"email":email})


def change_password_process(request):
    email = request.POST.get('email')
    pwd_one = request.POST.get('password_one')
    pwd_two = request.POST.get('password_two')
    try:
        user_obj = User.objects.get(email = email)
    except ObjectDoesNotExist:
        user_obj == None

    if user_obj != None:
        user_obj.password = pwd_two
        user_obj.save()
        return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect('/base/change_password')






