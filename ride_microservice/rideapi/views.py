from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
import json
import re
import requests
import csv
import datetime

# Create your views here.

def createRide(request):

    requestMade()

    if(request.method == 'POST'):
        json_body = json.loads(request.body)

        ride_created_by = json_body['created_by']
        timestamp = json_body['timestamp']
        source = json_body['source']
        destination = json_body['destination']

        s_name = "NULL"
        d_name = "NULL"

        timestamp_pattern = re.compile(r'^([1-9]|([012][0-9])|(3[01]))-([0]{0,1}[1-9]|1[012])-\d\d\d\d:[0-5][0-9]-[0-5][0-9]-[012]{0,1}[0-9]$')
        match = re.match(timestamp_pattern, timestamp)

        if not match:
            return JsonResponse({"message":"Invalid Timestamp"}, safe=False, status=400)

        if source == destination:
            return JsonResponse({"message":"Source and Destination cannot be same"}, safe=False, status=400)

        with open('AreaNameEnum.csv','r') as file:
            reader = csv.reader(file)
            for row in reader:
                if str(source) == str(row[0]):
                    s_name = row[1]
                if str(destination) == str(row[0]):
                    d_name = row[1]
        
        if ((s_name == "NULL") or (d_name == "NULL")):
            return JsonResponse({"message":"Invalid Enums"}, safe=False, status=400)
        
        # Check user
        # request_obj = {"table":"WebUser","username":ride_created_by}

        # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/read', json=request_obj)

        # r = requests.post('http://172.17.0.1:8080/api/v1/db/read', json=request_obj)

        # r = requests.get('http://127.0.0.1:8080/api/v1/users')
        r = requests.get('http://Assignment3-494350049.us-east-1.elb.amazonaws.com/api/v1/users')

        # r_users = r.json()['users_list']
        r_users = r.json()

        if ride_created_by not in r_users:
            return JsonResponse({"message":"Invalid username"},safe=False, status=400)
            
        else :
            request_obj = {"table":"Ride","username":ride_created_by,"source":source,"destination":destination,"timestamp":timestamp,"op":"insert"}

            # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/write', json=request_obj)
            
            r = requests.post('http://127.0.0.1:8000/api/v1/db/write', json=request_obj)

            if r.status_code == 200:
                return JsonResponse({},safe=False, status=201)
            elif r.status_code == 400:
                return JsonResponse({},safe=False, status=400)
            else:
                return JsonResponse({}, safe=False, status=501)

    elif (request.method == 'GET'):

        source = request.GET['source']
        destination = request.GET['destination']
        s_name = "NULL"
        d_name = "NULL"

        if source == destination:
            return JsonResponse({"message":"Source and Destination cannot be same"}, safe=False, status=400)

        with open('AreaNameEnum.csv','r') as file:
            reader = csv.reader(file)
            for row in reader:
                if str(source) == str(row[0]):
                    s_name = row[1]
                if str(destination) == str(row[0]):
                    d_name = row[1]
        
        if ((s_name == "NULL") or (d_name == "NULL")):
            return JsonResponse({"message":"Invalid Enums"}, safe=False, status=400)

        request_obj = {"table":"Ride","rideId":0,"source":source,"destination":destination,"read_all":"check"}

        # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/read', json=request_obj)

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        upcoming_rides = list()

        if r.status_code == 201:
            upcoming_rides = json.loads(r.json()['final'])
            return JsonResponse(upcoming_rides, safe=False, status=200)
        elif r.status_code == 200:
            return JsonResponse({}, safe=False, status=204)
        else:
            return JsonResponse({"message":"Some Error"}, safe=False, status=501)
    
    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def aboutRides(request,rideId):

    requestMade()

    if request.method == 'DELETE':

        request_obj = {"table":"Ride","rideId":rideId, "read_all":False}    #change

        # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/read', json=request_obj)

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        r_rides = r.json()['rides_list']

        if rideId not in r_rides:
            return JsonResponse({"message":"Invalid rideId"}, safe=False, status=400)

        else :

            request_obj = {"table":"Ride","rideId":rideId,"op":"delete"}
            # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/write', json=request_obj)

            r = requests.post('http://127.0.0.1:8000/api/v1/db/write', json=request_obj)

            if r.status_code == 200:
                return JsonResponse({},safe=False, status=200)
            
            elif r.status_code == 400:
                return JsonResponse({}, safe=False, status=400)
            else:
                return JsonResponse({},safe=False, status=501) # Unexpected
    
    elif request.method == 'POST':

        json_body = json.loads(request.body)
        username = json_body['username']

        request_obj = {"table":"Ride","rideId":rideId, "read_all":False}

        # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/read', json=request_obj)

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        r_rides = r.json()['rides_list']

        if rideId not in r_rides:
            return JsonResponse({"message":"Invalid rideId"}, safe=False, status=400)

        else :

            # request_obj = {"table":"WebUser","username":username}

            # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/read', json=request_obj)
            #check change
            # r = requests.post('http://172.17.0.1:8080/api/v1/db/read', json=request_obj)
            r = requests.get('http://Assignment3-494350049.us-east-1.elb.amazonaws.com/api/v1/users')


            # r_users = r.json()['users_list']
            r_users = r.json()    

            if username not in r_users:
                return JsonResponse({"message":"Invalid Username"}, safe=False, status=400)
            
            else :

                request_obj = {"table":"Ride","rideId":rideId,"username":username,"op":"update"}
                # r = requests.post('http://ec2-54-165-200-181.compute-1.amazonaws.com/api/v1/db/write', json=request_obj)

                r = requests.post('http://127.0.0.1:8000/api/v1/db/write', json=request_obj)

                if r.status_code == 202:
                    return JsonResponse({},safe=False, status=200)
                
                elif r.status_code == 400:
                    return JsonResponse({}, safe=False, status=400)
                else:
                    return JsonResponse({},safe=False, status=501) # Unexpected
    
    elif request.method == 'GET':

        request_obj = {"table":"Ride","rideId":rideId,"read_all":False}

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        r_rides = r.json()['rides_list']

        if rideId not in r_rides:
            return JsonResponse({"message":"Invalid rideId"}, safe=False, status=400)

        else :

            request_obj = {"table":"Ride","rideId":rideId,"read_all":True}

            r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

            r_allInfo = r.json()

            if r.status_code == 205:
                return JsonResponse(r_allInfo, safe=False, status=200)
            else:
                return JsonResponse({}, safe=False, status=400)
    else :
        
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def countRides(request):

    requestMade()

    if request.method == 'GET':
        
        request_obj = {"table":"Ride","read_all":"countRides"}

        r = requests.get('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        rides_list = r.json()['rides_list']

        if r.status_code == 200:

            rides_count = len(rides_list)
            
            return JsonResponse([rides_count], safe=False, status=200)

        else:

            return JsonResponse({}, safe=False, status=400)

    else:

        return JsonResponse({"message":"Wrong Method"}, safe=False, status=405)

def countHttp(request):

    if request.method == 'GET':

        with open('file.txt', 'r') as f_read:
            count = int(f_read.readline())

        return JsonResponse([count], safe=False, status=200)

    elif request.method == 'DELETE':
        
        with open('file.txt', 'w') as f_write:
            f_write.write("0")

        return JsonResponse({}, safe=False, status=200)
    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def clearDb(request):
    
    if request.method == 'POST':
        try:
            table = "Ride"
            cur_model = apps.get_model('rideapi',table)

            cur_model.objects.all().delete()

            return JsonResponse({"message":"Cleared Successfully"}, safe=False, status=200)

        except:
            return JsonResponse({"message":"Bad Request"}, safe=False, status=400)
    
    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def readDb(request):

    json_body = json.loads(request.body)
    table = json_body['table']
    
    cur_model = apps.get_model('rideapi', table)

    if table == "Ride":

        flag = json_body['read_all']

        if flag == "countRides":

            rides_list = cur_model.objects.all().values_list('ride_id',flat=True)
            rides_list = list(rides_list)

            response_dict = {"rides_list":rides_list}
            return JsonResponse(response_dict, safe=False, status=200)


        rideId = json_body['rideId']

        if flag == False:
            all_rides = cur_model.objects.values_list('ride_id',flat=True)
            rides_list = list(all_rides)

            response_dict = {"rides_list":rides_list}
            return JsonResponse(response_dict, safe=False, status=206)

        elif flag == True:
            all_info = cur_model.objects.get(ride_id = rideId)
            g_created = all_info.ride_created_by
            g_source = all_info.source
            g_destination = all_info.destination
            g_timestamp = all_info.timestamp
            g_riders_list = json.loads(all_info.riders_list)

            response_dict = {
                "ride_id":rideId,
                "ridecreated_by":g_created,
                "source":g_source,
                "destination":g_destination,
                "riders_list":g_riders_list,
                "timestamp":g_timestamp          
            }
            return JsonResponse(response_dict, safe=False, status=205)
        
        elif flag == "check":
            s = json_body["source"]
            d = json_body["destination"]
            
            upcoming_rides = cur_model.objects.filter(source=s,destination=d).values_list('ride_id','ride_created_by','timestamp')
            upcoming_rides = list(upcoming_rides)
            final = list()

            for i in upcoming_rides:
                timestamp = i[2]
                if (helper(timestamp)):
                    j = {}
                    j["rideId"] = i[0]
                    j["username"] = i[1]
                    j["timestamp"] = i[2]
                    final.append(j)

            if len(final) == 0:
                return JsonResponse({"final":final}, safe=False, status=200)
            else :
                final_arr = json.dumps(final)  
                return JsonResponse({"final":final_arr},safe=False, status=201)
    else :
        return JsonResponse({"message":"Model Not Found"}, safe=False, status=400) # Bad request

def helper(timestamp):

    time = timestamp.split(":")[1]
    date = timestamp.split(":")[0]

    tim_arr = time.split("-")
    tim = ""
    tim = tim + tim_arr[2]+":"+tim_arr[1]+":"+tim_arr[0]

    dat_arr = date.split("-") 
    dat = dat_arr[2] + "-" + dat_arr[1] + "-" +dat_arr[0]

    datetim = dat + " " +tim

    date_time = datetime.datetime.strptime(datetim, "%Y-%m-%d %H:%M:%S")

    present = datetime.datetime.now()

    if date_time > present:
        return True
    else :
        return False


def writeDb(request):

    json_body = json.loads(request.body)

    operation = json_body['op']
    table = json_body['table']

    if(table == "Ride"):

        if(operation == "insert"):
            ride_created_by = json_body["username"]
            source = json_body['source']
            destination = json_body['destination']
            timestamp = json_body['timestamp']
            riders_list = []
            riders_list = json.dumps(riders_list) # json

            try:
                cur_model = apps.get_model('rideapi', table)

                ride = cur_model(ride_created_by=ride_created_by,source=source,destination=destination,timestamp=timestamp,riders_list=riders_list)
                ride.save()

                return JsonResponse({"message":"Ride Created"}, safe=False, status=200)
            except:
                return JsonResponse({"message":"Ride Creation failed"}, safe=False, status=501)

        elif(operation == "delete"):
            rideId = json_body["rideId"]

            try:
                cur_model = apps.get_model('rideapi',table)

                ride_instance = cur_model.objects.get(ride_id=rideId)
                ride_instance.delete()

                return JsonResponse({"message":"Ride Deleted Successfully"},safe=False, status=200)

            except:
                return JsonResponse({"message":"Ride Delete Failed!"},safe=False, status=400)

        elif(operation == "update"):
            rideId = json_body["rideId"]
            username = json_body["username"]

            try:
                cur_model = apps.get_model('rideapi',table)
                ride_instance = cur_model.objects.get(ride_id=rideId)
                l = json.loads(ride_instance.riders_list)
                if username not in l:
                    l.append(username)
                l = json.dumps(l)
                ride_instance.riders_list = l
                ride_instance.save()
                return JsonResponse({},safe=False, status=202)                

            except:
                return JsonResponse({},safe=False, status=203)

        else :
            return JsonResponse({}, safe=False, status=302)


def requestMade():
    
    with open("file.txt", "r") as f_read:
        count = int(f_read.readline())

    count = count + 1

    with open("file.txt", "w") as f_write:
        f_write.write(str(count))
