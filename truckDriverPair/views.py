#############################################################
###########          Ship Easy                    ###########
###########          Project: ship easy           ###########
#############################################################
#  Program name: view.py
#  Auther: Vinie
#  Date: 27 - June - 2017
#  Time: 3:11 PM
#  M/V/C: files contain logic Pairing Of Truck and Driver with There table and status.
#############################################################
#############################################################

from django.shortcuts import render

# Create your views here.

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
from base.views import profile_for_all
from truck.models import Truck_data
from driver.models import Driver_add
from .models import Pair_and_status

def truck_driver_pair(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck = []
    truck_obj = Truck_data.objects.filter(pair_status = False).values('id','licanse_number')
    for item in truck_obj:
        truck.append(item)
    print("==========================",truck)
    driver = []
    driver_obj = Driver_add.objects.filter(pair_status = False).values('id','driver_name')
    for item in driver_obj:
        driver.append(item)
    print(driver)


    return render(request,'truck_driver_pair/truck_driver_pair.html',{'user':user,'new_list':new_list,'truck':truck,
                                                                      'driver':driver})

def pair_process(request):
    truck = request.POST.get('truck')
    driver = request.POST.get('driver')
    print("&&&&&&&&&&&",truck)
    print(")))))))))))))",driver)
    truck_obj = Truck_data.objects.get(id = truck )

    driver_obj = Driver_add.objects.get(id = driver)

    truck_obj.pair_status = True
    driver_obj.pair_status = True

    truck_obj.save()
    driver_obj.save()

    status_obj = Pair_and_status.objects.create(truck = truck_obj, driver = driver_obj)
    status_obj.empty_status = False
    status_obj.maintaion_status = True
    status_obj.break_down_status = False
    status_obj.save()
    return HttpResponseRedirect('/truck_drver_pair/status_table/')

def status_table(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    return render(request,'truck_driver_pair/status_table.html',{'user':user, "new_list" : new_list})

def status_table_data(request):
    status = []
    status_obj = Pair_and_status.objects.all()
    print("-------------",status_obj)
    for items in Pair_and_status.objects.all().values('id','truck','driver'):
        print(items['truck'])
        status_obj = Pair_and_status.objects.get(id = items['id'])
        truck_obj = Truck_data.objects.get(id = items['truck'])
        driver_obj = Driver_add.objects.get(id = items['driver'])
        status_check = ""
        if status_obj.maintaion_status is True:
            status_check = "Maintaned"

        elif status_obj.break_down_status is True:
            status_check = "braekdown"
        elif status_obj.empty_status is True:
            status_check = "Empty"

        items.update({"status":status_obj.maintaion_status, "truck_licen" : truck_obj.licanse_number,
                      "driver_name": driver_obj.driver_name, "mobile": driver_obj.mobile_number, 'status_check' : status_check})

        status.append(items)
        print("^^^^^^^^^^^^^", items)

    data = json.dumps(status)
    return HttpResponse(data, content_type='application/javascript')