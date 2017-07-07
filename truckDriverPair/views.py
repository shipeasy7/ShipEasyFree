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
from .models import Pair_and_status, Shipment_ids


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
    return HttpResponseRedirect('/truck_driver_pair/status_table/')


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
        elif status_obj.shipment_status is True:
            status_check = "Shipment"

        items.update({"status":status_obj.maintaion_status, "truck_licen" : truck_obj.licanse_number,
                      "driver_name": driver_obj.driver_name, "mobile": driver_obj.mobile_number, 'status_check' : status_check})

        status.append(items)
        print("^^^^^^^^^^^^^", items)

    data = json.dumps(status)
    return HttpResponse(data, content_type='application/javascript')


def status_change(request,id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    print("-------------",id)
    pair_obj = Pair_and_status.objects.get(id = id)
    driver_name = Driver_add.objects.get(licen_number = str(pair_obj.driver)).driver_name
    truck_licen = Truck_data.objects.get(licanse_number = str(pair_obj.truck)).licanse_number

    empty_status = pair_obj.empty_status
    maintance_status = pair_obj.maintaion_status
    breakdown_status = pair_obj.break_down_status
    shipment_status = pair_obj.shipment_status

    print("driver_name", truck_licen)
    return render(request,'truck_driver_pair/status_change.html',{"user": user,"new_list" : new_list, "pair_obj":pair_obj,
                                                                  "driver_name":driver_name, "truck_licen":truck_licen,
                                                                  "maintance_status": maintance_status,"empty_status":empty_status,
                                                                  "breakdown_status":breakdown_status,
                                                                  "shipment_status":shipment_status,"id" :id})


def status_change_process(request):
    id = request.POST.get("id")
    status = request.POST.get("active")
    print("---------------", status)
    print(id)
    pair_obj = Pair_and_status.objects.get(id = id)
    ggg = (request.POST.get('total_row_count'))
    print(ggg)
    # total_row_count = int(request.POST.get('total_row_count')) + 1
    # print("====================",total_row_count)
    if status == "maintain":
        pair_obj.maintaion_status = True
        pair_obj.empty_status = False
        pair_obj.shipment_status = False
        pair_obj.break_down_status = False
        pair_obj.save()
    elif status == "empty":
        pair_obj.maintaion_status = False
        pair_obj.empty_status = True
        pair_obj.shipment_status = False
        pair_obj.break_down_status = False
        pair_obj.save()
    elif status == "breakdown":
        pair_obj.maintaion_status = False
        pair_obj.empty_status = False
        pair_obj.shipment_status = False
        pair_obj.break_down_status = True
        pair_obj.save()
    elif status == "shipment":
        pair_obj.maintaion_status = False
        pair_obj.empty_status = False
        pair_obj.shipment_status = True
        pair_obj.break_down_status = False
        pair_obj.save()
    # print("77777777777777",total_row_count)
    if request.POST.get('total_row_count') != "":
        rows = request.POST.get('total_row_count')
        print("---------------------")
        total_row_count = int(request.POST.get('total_row_count')) + 1
        print("====================",total_row_count)
        for i in range(int(total_row_count)):
            ship_from = request.POST.get('form_'+str(i))
            ship_to = request.POST.get('to_'+str(i))
            name_of_customer = request.POST.get('customer_name_'+str(i))
            shipment_id = request.POST.get('shipment_id_'+str(i))
            contact = request.POST.get('contact_'+str(i))
            invoice_id = request.POST.get('invoice_id_'+str(i))
            print("--------#####-----------------",ship_from,ship_to,name_of_customer,shipment_id,contact)
            shipment_create = Shipment_ids.objects.create(pair_id = pair_obj, shipment_id = shipment_id,contact = contact,
                                                          ship_form = ship_from,ship_to = ship_to, name_of_customer = name_of_customer,
                                                          invoice_id = invoice_id)

        else:
            print("not any row")
    return HttpResponseRedirect('/truck_driver_pair/status_table/')


def unpair_status(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck = {}
    driver = {}
    paired_truck_driver = Pair_and_status.objects.all().values('id','driver_id','truck_id')
    print("--------", paired_truck_driver)
    driver = []
    truck = []
    for item in paired_truck_driver:
        print(item['driver_id'])
        driver.append(item['driver_id'])
        truck.append(item['truck_id'])
    name_driver = []
    for i in driver:
        driver_name = Driver_add.objects.filter(id = i).values('driver_name','id')
        for j in driver_name:
            name_driver.append(j)
        print(driver_name)

    licen_truck = []
    for i in truck:
        truck_licen = Truck_data.objects.filter(id = i).values('licanse_number','id')
        for j in truck_licen:
            licen_truck.append(j)

    return render(request,'truck_driver_pair/unpair_status.html',{"user": user,"new_list" : new_list,'truck':licen_truck,'driver':name_driver})


def unpair_status_process(request):
    truck = request.POST.get('truck')
    driver = request.POST.get('driver')
    print("-----------", truck)
    print("-----------", driver)
    truck_obj = Truck_data.objects.get(licanse_number = truck)
    truck_obj.pair_status = False
    truck_obj.save()
    driver_obj = Driver_add.objects.get(driver_name = driver)
    driver_obj.pair_status = False
    driver_obj.save()
    print(truck_obj)
    pair_table_obj = Pair_and_status.objects.get(truck_id = truck_obj.id)
    print("------------------------------@@@@ss", pair_table_obj)
    pair_table_obj.delete()

    return HttpResponseRedirect('/truck_driver_pair/status_table/')


def licen_through_driver_name(request,licanse_numbers):
    print("))))))))))@", licanse_numbers)
    truck_obj = Truck_data.objects.get(licanse_number = licanse_numbers).id
    print("truck obj", truck_obj)
    pair_obj = Pair_and_status.objects.get(truck_id = truck_obj).driver_id
    print("pair obj",pair_obj )
    driver_name = Driver_add.objects.get(id = pair_obj).driver_name
    print(driver_name)

    data = json.dumps(driver_name)
    return HttpResponse(data, content_type='application/javascript')


def find_licen_from_driver(request, driver_name):
    print(driver_name)
    driver_obj = Driver_add.objects.get(driver_name = driver_name).id
    pair_obj = Pair_and_status.objects.get(driver_id = driver_obj).truck_id
    truck_licenc = Truck_data.objects.get(id = pair_obj).licanse_number
    data = json.dumps(truck_licenc)
    return HttpResponse(data, content_type='application/javascript')


