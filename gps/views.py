#############################################################
###########          Ship Easy                    ###########
###########          Project: ship easy           ###########
#############################################################
#  Program name: view.py
#  Auther: Vinie
#  Date: 26 - June - 2017
#  Time: 12:31 PM
#  M/V/C: files contain logic fill cunsaltant Form print it and upload and track
# mobile number .
#############################################################
#############################################################



from django.shortcuts import render
import os

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa# to convert html to pdf

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
import json,requests
import time
import threading
from reportlab.pdfgen import canvas

from driver.models import Driver_add
from truck.models import Truck_data
from gps.models import Aproved_mobile_number, GPS_status, RowData

from base.views import profile_for_all


def gps_licen_input(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck = []
    truck_obj = Truck_data.objects.filter().values('id','licanse_number','mobile_number')
    for item in truck_obj:
        truck.append(item)
    print("==========================",truck)
    driver = []
    driver_obj = Driver_add.objects.filter().values('id','driver_name','licen_number')
    for item in driver_obj:
        driver.append(item)
    print(driver)

    return render(request,'gps/gps_input_form.html',{'user':user,'new_list':new_list, 'truck':truck,'driver':driver})


def driver_mobile_number(request, number):
    get_mobile = []
    user_data = Driver_add.objects.get(licen_number=number)
    mobile = user_data.mobile_number
    get_mobile.append(mobile)
    operator = user_data.operator
    get_mobile.append(operator)

    data = json.dumps(get_mobile)
    return HttpResponse(data, content_type='application/javascript')

def truck_mobile_number(request, number):
    get_mobile = []
    user_data = Truck_data.objects.get(licanse_number = number)
    mobile = user_data.mobile_number
    get_mobile.append(mobile)
    operator = user_data.operator
    get_mobile.append(operator)

    data = json.dumps(get_mobile)
    return HttpResponse(data, content_type='application/javascript')

def print_form(request):


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    p = canvas.Canvas(response)

    get_oerator = request.POST.get('operator')
    licen_id = request.POST.get('truck')
    licen_id2 = request.POST.get('driver')
    print("---------------------------------",licen_id)
    print("---------------------------------",licen_id2)
    date = (time.strftime("%d/%m/%Y"))
    print("---------",date)

    if licen_id2 == "":
        try:
            truck_obj = Truck_data.objects.get(licanse_number=licen_id)
        except ObjectDoesNotExist:
            truck_obj == None

        if truck_obj != None:
            print("in Truck")
            if get_oerator == "Airtel":
                data = {'date': date, 'obj':truck_obj}
                template = get_template('operator_forms/airtel_form.html')
                html = template.render(Context(data))
                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')
                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')
                # return render(request,'operator_forms/airtel_form.html',{'date': date, 'obj':truck_obj})
            elif get_oerator == "Vodaphone":

                data = {'date': date, 'obj':truck_obj}
                template = get_template('operator_forms/vodaphone.html')
                html = template.render(Context(data))

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')

                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')
                # return render(request,'operator_forms/vodaphone.html',{'date': date, 'obj':truck_obj})
            elif get_oerator == "Idea":

                data = {'date': date, 'obj':truck_obj}
                template = get_template('operator_forms/idea.html')
                html = template.render(Context(data))

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')

                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')
                # return render(request,'operator_forms/idea.html',{'date': date, 'obj':truck_obj})

    else:
        pass


    if licen_id == "":
        try:
            driver_obj = Driver_add.objects.get(licen_number = licen_id2)
        except ObjectDoesNotExist:
            driver_obj == None
        if driver_obj != None:
            if get_oerator == "Airtel":

                data = {'date': date, 'obj':driver_obj}
                template = get_template('operator_forms/airtel_form.html')
                html = template.render(Context(data))

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')

                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')
                # return render(request, 'operator_forms/airtel_form.html',{'date':date, 'obj':driver_obj})
            elif get_oerator == "Vodafone":

                data = {'date': date, 'obj':driver_obj}
                template = get_template('operator_forms/vodaphone.html')
                html = template.render(Context(data))

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')

                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')

                # return render(request, 'operator_forms/vodaphone.html', {'date': date, 'obj': driver_obj})
            elif get_oerator == "Idea":

                data = {'date': date, 'obj':driver_obj}
                template = get_template('operator_forms/idea.html')
                html = template.render(Context(data))

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')

                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')
                # return render(request, 'operator_forms/idea.html', {'date': date, 'obj': driver_obj})


            else:
                pass



def upload_scaned_documents(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    driver = []
    truck = []
    driver_obj = Driver_add.objects.all().values('mobile_number','driver_name')
    truck_obj = Truck_data.objects.all().values('mobile_number','licanse_number')
    for i in driver_obj:
        print("@@@@@@", type(i))
        dic = i
        mobile = dic['mobile_number']
        print("+++++++++++", mobile)
        driver_obj = Driver_add.objects.get(mobile_number = mobile)
        print("&&&&&&&&", driver_obj)
        driver.append(driver_obj)
    for i in truck_obj:
        print("@@@@@@", type(i))
        dic = i
        mobile = dic['mobile_number']
        print("+++++++++++", mobile)
        truck_obj = Truck_data.objects.get(mobile_number = mobile)
        print("&&&&&&&&", truck_obj)
        truck.append(truck_obj)
    status = (request.GET.get('status'))
    if status == "added":
        message = "Your Documents sended sucessfully If you have any other the you can send"
    else:
        message = ""
    return render(request,'gps/gps_send_form.html',{'user': user, 'driver':driver , 'truck':truck,
                                                    'new_list': new_list, 'message':message})

def mail_documents(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    if request.method == "POST":
        # this checks that a file exists
        if len(request.FILES) != 0:
            file1 = request.FILES['file1']
            file1str = file1.read()
            file_type = str(request.FILES['file1'].content_type)
            email_msg = EmailMessage(subject="Activate user Mobile Number To Track", body="Activate user",
                                     from_email="support@shipeasy.in", to=["sales@shipeasy.in"])
            # need to try to attach the file, using the attach method
            try:
                email_msg.attach('file1', file1str, file_type)
            except Exception as e:
                print(str(e))
            email_msg.send()

    # return render(request,'gps/gps_send_form.html',{"message":"your mail send sucess fully", 'user':user, 'new_list':new_list})
    return HttpResponseRedirect('/gps/upload_scaned_documents/?status=added')


def tracking_device(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    truck = []
    aproved_mobile_number = Aproved_mobile_number.objects.all().values('mobile_number')
    for i in Aproved_mobile_number.objects.all().values('mobile_number'):
        print("@@@@@@",type(i))
        dic = i
        mobile = dic['mobile_number']
        print("+++++++++++",mobile)
        truck_obj = Truck_data.objects.get(mobile_number = mobile)
        print("&&&&&&&&", truck_obj)
        # for item in truck_obj.licanse_number:
        #     truck.append(item)
        truck.append(truck_obj)
        print("==========================",truck)
    return render(request,'gps/track_device.html',{'user':user , "truck": truck,"new_list" : new_list})

def xyz(mobile,id):
    print("***********************",mobile)
    print("@@@@@@@@@@@@@@@@@@@@@@@@", id)
    dummy_obj = GPS_status.objects.get(mobile_number = mobile, id = id)
    url = "http://demolaas.accelerite.com/locationstudio/location/v1/queries/location?address=tel%3A%2B" + mobile + ",tel%3A%2B5678906781&requestedAccuracy=5000&acceptableAccuracy=5000"
    username = 'shipeasy'
    password = 'Shipeasy@123'

    response = requests.get(url,
                            auth=(username, password))
    list_data = []
    json_data = {}
    x = response.json()
    print('_______________________', x)
    for i in range(0, 2):
        address = (x['terminalLocationList']['terminalLocation'][i]['address'])
        new_address = (address[-10:])
        longitude = (x['terminalLocationList']['terminalLocation'][i]['currentLocation']['longitude'])

        altitude = (x['terminalLocationList']['terminalLocation'][i]['currentLocation']['altitude'])
        latitude = (x['terminalLocationList']['terminalLocation'][i]['currentLocation']['latitude'])
        timestamp = (x['terminalLocationList']['terminalLocation'][i]['currentLocation']['timestamp'])

    dummy_obj.longitude = longitude
    dummy_obj.latitude = latitude
    dummy_obj.altitude = altitude
    dummy_obj.timestamp = timestamp

    dummy_obj.save()

def dummy_data():
    threading.Timer(100000000, dummy_data).start()
    truck = []
    mobiles = []
    # for item in Truck_info_data.objects.all().values('id','mobile_number'):
    for item in Aproved_mobile_number.objects.all().values('mobile_number'):
        print("----------",item)

        truck.append(item)
    print(truck)
    truck_new = truck[0]
    print(truck_new)
    for i in range (0, len(truck)):
        dic = truck[i]
        mobile = dic['mobile_number']
        mobiles.append(mobile)
        print(mobiles)

        dummy_obj = GPS_status.objects.create(mobile_number = mobile )
        mobile_num = dummy_obj.mobile_number
        id = dummy_obj.id
        xyz(mobile_num,id )

    for item in mobiles:
        print("-----",item)


dummy_data()

def display_lat_long(request):
    user = request.session.get('user')
    new_list = profile_for_all(request)
    mobile = request.POST.get("truck")
    truck_obj = Truck_data.objects.get(mobile_number= mobile).licanse_number
    dic = {}
    lat_long = []
    lat_long_obj = GPS_status.objects.filter(mobile_number = mobile).values('id','licen_number','longitude','altitude',
                                                   'latitude','timestamp', 'driver_name')

    for item in lat_long_obj:
        item.update({"licen_number": truck_obj})
        lat_long.append(item)
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", lat_long)

    print("=====================",lat_long)
    return render(request, 'gps/gps_table.html', {"data" : lat_long ,'user': user, 'new_list':new_list })


def gps_lat_long(request):
    mobile_number = request.POST.get('search')
    print("--------------------", mobile_number)
    # x= (RowData.objects.all().values('mobile_number'))
    #    for i in :
    #        print("--------------------",i)
    row_mobile = RowData.objects.filter(mobile_number = mobile_number)

    print("----", row_mobile)
    if row_mobile.exists():
        main = []
        h = []
        g = []
        row_data_obj = RowData.objects.filter(mobile_number = mobile_number).values('lat', 'long')
        print(row_data_obj)
        for i in row_data_obj:
            h.append(i['lat'])
            g.append(i['long'])
        for a, b in zip(g, h):
            main.append([b, a])

        print("=====================+", main)
        return render(request, 'gps/google_map.html', {'x': main})

    else:
        main = [[19.111202, 72.870912], [19.111202, 72.870912]]
        return render(request, 'gps/google_map.html', {'x': main})
