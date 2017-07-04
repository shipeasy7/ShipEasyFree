#############################################################
###########          Ship Easy                    ###########
###########          Project: ship easy           ###########
#############################################################
#  Program name: view.py
#  Auther: Vinie
#  Date: 26 - June - 2017
#  Time: 10:26 AM
#  M/V/C: files contain logic Create Driver , edit truck info and truck Tables.
#############################################################
#############################################################


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.core.mail import EmailMessage

import json
import os

from .models import Driver_add
# Create your views here.

from base.views import profile_for_all

def add_driver_one(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    return render(request,'driver/add_driver_one.html',{'user':user,'new_list':new_list})


def add_driver_one_process(request):
    date = request.POST.get('date')
    # new_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
    licen_number = request.POST.get('licen_number')
    driver_name = request.POST.get('name')
    licen_type = request.POST.get('licen_type')
    mobile_number = request.POST.get('mobile_number')
    operator = request.POST.get('operator')

    id = request.POST.get("id")

    files1 = request.FILES.get('file1')
    files2 = request.FILES.get('file2')

    filename1 = files1._get_name()
    filename2 = files2._get_name()
    database_finle_name1 = licen_number+"_"+filename1
    database_finle_name2 = licen_number + "_" + filename2
    filename1 = filename1.replace(' ', '_')
    filename2 = filename2.replace(' ', '_')
    fd1 = open(
        '%s/%s' % (settings.MEDIA_ROOT + '/driver/', str(licen_number) + '_' + 'pan' + '_' + str(filename1)),
        'wb')
    fd2 = open(
        '%s/%s' % (settings.MEDIA_ROOT + '/driver/', str(licen_number) + '_' + 'adhar' + '_' + str(filename2)),
        'wb')

    for chunk in files1.chunks():
        fd1.write(chunk)
    fd1.close()
    for chunk in files2.chunks():
        fd2.write(chunk)
    fd2.close()
    if id == "":
        new_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

        driver_obj = Driver_add.objects.create(licen_number=licen_number, driver_name=driver_name,
                                               date=new_date, licaen_type=licen_type, mobile_number=mobile_number,
                                               operator=operator, pan_card_pic = database_finle_name1,
                                               adhar_card = database_finle_name2)
        driver_id = driver_obj.id

        if 'file1' in request.FILES:
            driver_obj.licanse_image = request.FILES.get('file1')
        else:
            driver_obj.image = 'no_image.png'
        return HttpResponseRedirect('/driver/add_driver_two/' + str(driver_id))

    else:
        driver_obj = Driver_add.objects.get(id = id)
        driver_obj.licen_number = licen_number
        driver_obj.driver_name = driver_name
        print("d]",driver_name)
        driver_obj.licaen_type = licen_type
        driver_obj.mobile_number = mobile_number
        driver_obj.operator = operator
        print("====================",date)
        new_date = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
        print("====================================",new_date)
        driver_obj.date = new_date
        driver_obj.pan_card_pic = database_finle_name1
        driver_obj.adhar_card = database_finle_name2
        driver_obj.save()

        return HttpResponseRedirect('/driver/edit_driver_two/' + str(id))


def add_driver_two(request,id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    return render(request,'driver/add_driver_two.html',{'user':user, 'id' : id, 'new_list':new_list})


def add_driver_two_process(request):
    id = request.POST.get('id')
    p_one = request.POST.get('preference_one')
    p_two = request.POST.get('preference_two')
    a_one = request.POST.get('address_one')
    a_two = request.POST.get('address_two')
    mobile_one = request.POST.get('mobile_number_one')
    mobile_two = request.POST.get('mobile_number_two')
    update_id = request.POST.get('update_id')
    if update_id == "":
        try:
            driver_obj = Driver_add.objects.get(id = id)
        except ObjectDoesNotExist:
            driver_obj == None
        if driver_obj != None:
            driver_obj.reference_one = p_one
            driver_obj.reference_two = p_two
            driver_obj.address_one =a_one
            driver_obj.address_two = a_two
            driver_obj.ref_moblie_one = mobile_one
            driver_obj.ref_moblie_two = mobile_two
            driver_obj.save()
        return HttpResponseRedirect('/driver/driver_table/?status=added')
    else:
        try:
            driver_obj = Driver_add.objects.get(id = update_id)
        except ObjectDoesNotExist:
            driver_obj == None
        if driver_obj != None:
            driver_obj.reference_one = p_one
            driver_obj.reference_two = p_two
            driver_obj.address_one =a_one
            driver_obj.address_two = a_two
            driver_obj.ref_moblie_one = mobile_one
            driver_obj.ref_moblie_two = mobile_two
            driver_obj.save()
        return HttpResponseRedirect('/driver/driver_table/?status=edited')



def driver_table(request):
    user = request.session.get('user')
    status = (request.GET.get('status'))
    if status == "added":
        message = "Added Suceess fully"
    elif status == "edited":
        message = "driver Info Edited"
    elif status == "no":
        message = "Driver Allready paird Please Unpair It to deleate "
    else:
        message = ""
    new_list = profile_for_all(request)
    return render(request, 'driver/driver_table.html', {'user': user, 'message':message, 'new_list':new_list})


def all_driver(request):
    driver = []
    for item in Driver_add.objects.all().values('id', 'licen_number', 'driver_name', 'licaen_type',
                                                'mobile_number', 'operator','reference_one',
                                                'ref_moblie_one', 'reference_two', 'ref_moblie_two'):
        driver.append(item)

    data = json.dumps(driver)
    return HttpResponse(data, content_type='application/javascript')


def edit_driver(request, id):
    user = request.session.get('user')
    driver_obj = Driver_add.objects.get(id = id)
    print(driver_obj)
    new_list = profile_for_all(request)

    image_name = str(driver_obj.pan_card_pic)
    print("image_name", image_name)
    logo = os.listdir(settings.MEDIA_ROOT + '/driver/')
    print(image_name)
    x = (image_name.split('_', 1))
    print("XXXXXXXXXXXXXXXXXXX",x)
    print("--------------------------------------------------------",driver_obj.pan_card_pic)
    new_image = x[1]
    pan_list = []
    print("/////////", (str(driver_obj.licen_number) + '_' + 'pan' + str(new_image)))
    for items in logo:
        if items.startswith(str(driver_obj.licen_number) + '_' + 'pan' + "_" + new_image):
            pan_list.append({'link': '/media/driver/' + items})
            print("////////", pan_list)

    image_name = str(driver_obj.adhar_card)
    print("image_name", image_name)
    logo = os.listdir(settings.MEDIA_ROOT + '/driver/')
    print(image_name)
    x = (image_name.split('_', 1))
    print("XXXXXXXXXXXXXXXXXXX", x)
    print("--------------------------------------------------------", driver_obj.licen_number)
    new_image = x[1]
    adhar_list = []
    print("/////////", (str(driver_obj.licen_number) + '_' + 'adhar' + str(new_image)))
    for items in logo:
        if items.startswith(str(driver_obj.licen_number) + '_' + 'adhar' + "_" + new_image):
            adhar_list.append({'link': '/media/driver/' + items})
            print("////////", adhar_list)

    return render(request, 'driver/add_driver_one.html', {"driver_obj": driver_obj, 'user': user, 'pan':pan_list,
                                                          "image_name" : x , 'adhar_pic': adhar_list})


def edit_driver_two(request, id):
    user = request.session.get('user')
    driver_obj = Driver_add.objects.get(id=id)
    print(driver_obj)
    new_list = profile_for_all(request)
    return render(request, 'driver/add_driver_two.html', {"driver_obj": driver_obj, 'user': user,'new_list':new_list})


def delete_driver(request,id):
    driver_obj = Driver_add.objects.get(id = id)
    if driver_obj.pair_status == True:
        return HttpResponseRedirect('/driver/driver_table/?status=no')
    else:

        driver_obj.delete()
    return HttpResponseRedirect('/driver/driver_table')



