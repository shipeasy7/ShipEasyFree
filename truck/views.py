#############################################################
###########          Ship Easy                    ###########
###########          Project: ship easy           ###########
#############################################################
#  Program name: view.py
#  Auther: Vinie
#  Date: 25 - June - 2017
#  Time: 5:43 PM
#  M/V/C: files contain logic Create New Truck .
#############################################################
#############################################################
import os

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
import json
from glob import glob
from django.core.mail import EmailMessage

from .models import Truck_data

from django.shortcuts import render

from base.views import profile_for_all

# Create your views here.
def add_truck_one(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    return render(request,'truck/add_truck_one.html',{'user':user,'new_list':new_list})


def add_truck_one_process(request):
    license_number = request.POST.get("licanse_number")
    truck_oem = request.POST.get("truck_oem")
    model = request.POST.get("truck_model")
    wheels = request.POST.get("wheels")
    axle_type = request.POST.get("axle_type")
    type = request.POST.get("type")
    id = request.POST.get("id")
    truck_type = request.POST.get("type")

    print("-------------", axle_type,type)
    fiele_path = request.POST.get("file1")
    print("hhhhhhhhhhhh"),
    files1 = request.FILES.get('file1')
    print("--------------",files1)
    files2 = request.FILES.get('file2')
    filename1 = files1._get_name()
    filename2 = files2._get_name()
    filename1 = filename1.replace(' ', '_')
    filename2 = filename2.replace(' ', '_')
    database_finle_name1 = license_number+"_"+filename1
    database_finle_name2 = license_number + "_" + filename2
    fd1 = open(
        '%s/%s' % (settings.MEDIA_ROOT + '/truck/', str(license_number) + '_' + 'licen' + '_' + str(filename1)),
        'wb')
    fd2 = open('%s/%s' % (settings.MEDIA_ROOT + '/truck/', str(license_number) + '_' + 'roc' + '_' + str(filename2)),
               'wb')


    for chunk in files1.chunks():
        fd1.write(chunk)
    fd1.close()
    for chunk in files2.chunks():
        fd2.write(chunk)
    fd1.close()
    print("-----------------",id)

    if id == "":
        print("in create")
        truck_obj = Truck_data.objects.create(licanse_number = license_number, truck_oem = truck_oem, model = model,
                                              wheels = wheels, axle_type= axle_type,
                                              licanse_image = database_finle_name1, roc_image = database_finle_name2,
                                              truck_type = truck_type)
        truck_id = truck_obj.id
        return HttpResponseRedirect('/truck/add_truck_two/' + str(truck_id))
    else:
        print("in update")
        truck_obj = Truck_data.objects.get(id = id)
        truck_obj.licanse_number = license_number
        truck_obj.truck_oem = truck_oem
        truck_obj.model = model
        truck_obj.wheels = wheels
        truck_obj.axle_type = axle_type
        truck_obj.truck_type = type
        truck_obj.licanse_image = database_finle_name1
        truck_obj.roc_image =database_finle_name2
        truck_obj.truck_type = truck_type
        truck_obj.save()

        return HttpResponseRedirect('/truck/edit_truck_two/' + str(id))


def add_truck_two(request, id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    return render(request, 'truck/add_truck_two.html', {'user': user, 'truck_id': id, 'new_list':new_list})


def add_truck_two_process(request):
    id = request.POST.get('id')
    truck_type = request.POST.get('truck_type')
    truck_capacity = request.POST.get('truck_capacity')
    truck_length = request.POST.get('truck_length')
    mobile_number = request.POST.get('mobile_number')
    operator = request.POST.get('operator')

    update_id = request.POST.get('update_id')
    print("-------",update_id)
    if update_id == "":
        truck_obj = Truck_data.objects.get(id = id)
        print("------------",truck_obj)
        # truck_obj.truck_type = truck_type
        truck_obj.truck_capacity = truck_capacity
        truck_obj.truck_lemgth = truck_length
        truck_obj.mobile_number = mobile_number
        truck_obj.operator = operator

        truck_obj.save()

        return HttpResponseRedirect('/truck/add_truck_three/' + id)
    else:
        truck_obj = Truck_data.objects.get(id=update_id)
        print("------------", truck_obj)
        # truck_obj.truck_type = truck_type
        truck_obj.truck_capacity = truck_capacity
        truck_obj.truck_lemgth = truck_length
        truck_obj.mobile_number = mobile_number
        truck_obj.operator = operator
        truck_obj.save()
        return HttpResponseRedirect('/truck/edit_truck_three/' + update_id)


def add_truck_three(request,id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    return render(request,'truck/add_truck_three.html',{'user':user, 'truck_id':id, 'new_list':new_list})


def add_truck_three_process(request):
    id = request.POST.get('id')
    print(id)
    owner_name = request.POST.get('owener_name')
    contact = request.POST.get('contact')
    date = request.POST.get('date')
    new_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
    update_id = request.POST.get('update_id')
    if update_id == "":
        try:
            truck_obj = Truck_data.objects.get(id=id)
        except ObjectDoesNotExist:
            truck_obj = None
        if truck_obj != None:
            license_number = truck_obj.licanse_number

            files1 = request.FILES.get('file1')
            files2 = request.FILES.get('file2')
            filename1 = files1._get_name()
            filename2 = files2._get_name()
            database_finle_name1 = license_number + "_" + filename1
            database_finle_name2 = license_number + "_" + filename2
            filename1 = filename1.replace(' ', '_')
            filename2 = filename2.replace(' ', '_')
            fd1 = open(
                '%s/%s' % (settings.MEDIA_ROOT + '/truck/', str(license_number) + '_' + 'pan' + '_' + str(filename1)),
                'wb')
            fd2 = open(
                '%s/%s' % (settings.MEDIA_ROOT + '/truck/', str(license_number) + '_' + 'fitness' + '_' + str(filename2)),
                'wb')

            for chunk in files1.chunks():
                fd1.write(chunk)
            fd1.close()
            for chunk in files2.chunks():
                fd2.write(chunk)
            fd2.close()

            truck_obj.owener_name = owner_name
            truck_obj.conatact = contact
            truck_obj.date_of_fitnace_certificate = new_date
            # truck_obj.fitness_certificate = fd2
            truck_obj.pan_card_pic = database_finle_name1
            truck_obj.fitness_certificate = database_finle_name2
            truck_obj.save()
        else:
            print("user Not found please urls Id")
        return HttpResponseRedirect('/truck/truck_table/?status=added')
    else:
        try:
            truck_obj = Truck_data.objects.get(id=update_id)
        except ObjectDoesNotExist:
            truck_obj = None
        if truck_obj != None:
            license_number = truck_obj.licanse_number

            files1 = request.FILES.get('file1')
            files2 = request.FILES.get('file2')
            filename1 = files1._get_name()
            filename2 = files2._get_name()
            database_finle_name1 = license_number + "_" + filename1
            database_finle_name2 = license_number + "_" + filename2
            filename1 = filename1.replace(' ', '_')
            filename2 = filename2.replace(' ', '_')
            fd1 = open(
                '%s/%s' % (settings.MEDIA_ROOT + '/truck/', str(license_number) + '_' + 'pan' + '_' + str(filename1)),
                'wb')
            fd2 = open(
                '%s/%s' % (
                settings.MEDIA_ROOT + '/truck/', str(license_number) + '_' + 'fitness' + '_' + str(filename2)),
                'wb')

            for chunk in files1.chunks():
                fd1.write(chunk)
            fd1.close()
            for chunk in files2.chunks():
                fd2.write(chunk)
            fd2.close()

            truck_obj.owener_name = owner_name
            truck_obj.conatact = contact
            truck_obj.date_of_fitnace_certificate = new_date
            truck_obj.pan_card_pic = database_finle_name1
            truck_obj.fitness_certificate = database_finle_name2

            truck_obj.save()
        else:
            print("user Not found please urls Id")
        return HttpResponseRedirect('/truck/truck_table/?status=edited')


def truck_table(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    status = (request.GET.get('status'))
    if status == "added":
        message = "Truck Added Suceess fully"
    elif status == "edited":
        message = "Truck Info Edited"
    elif status == "not":
        message = "Truck Allready paird Please Unpair It to deleate"


    else:
        message = ""
    return render(request,'truck/truck_table.html',{'user':user, 'message':message,'new_list':new_list})

def all_truck(request):
    truck = []
    for item in Truck_data.objects.all().values('id', 'licanse_number', 'mobile_number',
                                                     'truck_capacity','truck_type','wheels','truck_oem',
                                                     'owener_name','axle_type', 'model'):
        truck.append(item)

    data = json.dumps(truck)
    return HttpResponse(data, content_type='application/javascript')


def edit_truck(request, id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck_obj = Truck_data.objects.get(id = id)
    print(truck_obj)

    image_name = str(truck_obj.licanse_image)
    print("image_name", image_name)
    logo = os.listdir(settings.MEDIA_ROOT + '/truck/')
    file_path = os.path.abspath(image_name)
    print(file_path)
    print(image_name)
    x = (image_name.split('_', 1))
    print("XXXXXXXXXXXXXXXXXXX", x)
    print("--------------------------------------------------------", truck_obj.licanse_image)
    new_image = x[1]
    licen_list = []
    print("/////////", (str(truck_obj.licanse_number) + '_' + 'licen' + str(new_image)))
    for items in logo:
        if items.startswith(str(truck_obj.licanse_number) + '_' + 'licen' + "_" + new_image):
            licen_list.append({'link': '/media/truck/' + items})
            print("////////", licen_list)

    image_name = str(truck_obj.roc_image)
    print("image_name", image_name)
    logo = os.listdir(settings.MEDIA_ROOT + '/truck/')
    print(image_name)
    x = (image_name.split('_', 1))
    print("XXXXXXXXXXXXXXXXXXX", x)
    print("------------------------------------------>>>>>>>>--------------", truck_obj.licanse_number)
    new_image = x[1]
    roc_list = []
    print("/////////", (str(truck_obj.licanse_number) + '_' + 'roc' + str(new_image)))
    for items in logo:
        if items.startswith(str(truck_obj.licanse_number) + '_' + 'roc' + "_" + new_image):
            roc_list.append({'link': '/media/truck/' + items})
            print("////////", roc_list)

    return render(request,'truck/add_truck_one.html',{"truck_obj":truck_obj,'user':user,'new_list':new_list,
                                                      "licen":licen_list, 'roc':roc_list , "fiele_path": file_path})

def edit_truck_two(request, id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck_obj = Truck_data.objects.get(id = id)
    print(truck_obj)
    return render(request,'truck/add_truck_two.html',{"truck_obj":truck_obj,'user':user,'new_list':new_list })


def edit_truck_three(request,id):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck_obj = Truck_data.objects.get(id = id)
    print(truck_obj)


    print("&&&&&&&&&&&&&&", truck_obj.date_of_fitnace_certificate)
    get_date = truck_obj.date_of_fitnace_certificate

    set_det = datetime.strptime(str(get_date),'%Y-%m-%d').strftime('%m/%d/%Y')



    image_name = str(truck_obj.pan_card_pic)
    print("image_name", image_name)
    logo = os.listdir(settings.MEDIA_ROOT + '/truck/')
    file_path = os.path.abspath(image_name)
    print(file_path)
    print(image_name)
    x = (image_name.split('_', 1))
    print("XXXXXXXXXXXXXXXXXXX", x)
    print("--------------------------------------------------------", truck_obj.pan_card_pic)
    new_image = x[1]
    pan_list = []
    print("/////////", (str(truck_obj.licanse_number) + '_' + 'pan' + str(new_image)))
    for items in logo:
        if items.startswith(str(truck_obj.licanse_number) + '_' + 'pan' + "_" + new_image):
            pan_list.append({'link': '/media/truck/' + items})
            print("////////", pan_list)

    image_name = str(truck_obj.fitness_certificate)
    print("image_name", image_name)
    logo = os.listdir(settings.MEDIA_ROOT + '/truck/')
    print(image_name)
    x = (image_name.split('_', 1))
    print("XXXXXXXXXXXXXXXXXXX", x)
    print("------------------------------------------>>>>>>>>--------------", truck_obj.licanse_number)
    new_image = x[1]
    fitnes_list = []
    print("/////////", (str(truck_obj.licanse_number) + '_' + 'fitness' + str(new_image)))
    for items in logo:
        if items.startswith(str(truck_obj.licanse_number) + '_' + 'fitness' + "_" + new_image):
            fitnes_list.append({'link': '/media/truck/' + items})
            print("////////", fitnes_list)

    return render(request,'truck/add_truck_three.html',{"truck_obj":truck_obj,'user':user,'new_list':new_list,
                                                        'pan_list': pan_list, "fitnes_list" : fitnes_list, "set_det": set_det})





def delete_truck(request,id):
    truck_obj = Truck_data.objects.get(id = id)
    if truck_obj.pair_status == True:
        return HttpResponseRedirect('/truck/truck_table/?status=not')
    else:
        truck_obj.delete()

    return HttpResponseRedirect('/truck/truck_table/')

