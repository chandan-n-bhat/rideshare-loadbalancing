from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
import json
import re
import requests

# Create your views here.

def createUser(request):

    requestMade()

    if request.method == 'PUT':
        json_body = json.loads(request.body)

        username = json_body['username']
        password = json_body['password']

        sha_pattern = re.compile(r'\b[0-9a-f]{40}\b')
        match = re.match(sha_pattern, password)

        if match :
            pass
        else :
            response_obj = {"message":"Password not in SHA1 format"}
            return JsonResponse(response_obj,safe=False,status=400)

        request_obj = {"table":"WebUser","operation":"get","username":username}

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        if r.status_code == 200:

            response_obj = {"message":"Username already present"}
            return JsonResponse(response_obj, safe=False, status=400)
        
        elif r.status_code == 400:

            request_obj = {"table":"WebUser","operation":"insert","username":username,"password":password}
            
            r = requests.post('http://127.0.0.1:8000/api/v1/db/write', json=request_obj)

            if r.status_code == 200:
                return JsonResponse({"message":"Successfully Added User"}, safe=False, status=201)
            elif r.status_code == 400:
                return JsonResponse({"message":"Oops... Operation Failed"}, safe=False, status=400)
            else:
                return JsonResponse({"message":"Unknown Error"}, safe=False, status=400)

        else:
            return JsonResponse({"message":"Unknown Error Occured"}, safe=False, status=400)


    elif request.method == 'GET':

        request_obj = {"table":"WebUser","operation":"all"}

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)
        
        if r.status_code == 200 :
            r_users = r.json()['users_list']

            if len(r_users) == 0:
                return JsonResponse({}, safe=False, status=204)
            
            else:
                return JsonResponse(r_users, safe=False, status=200)
        
        else :
            return JsonResponse({}, safe=False, status=400)

    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)

def removeUser(request,username):

    requestMade()

    if request.method == 'DELETE':
        
        request_obj = {"table":"WebUser","operation":"get","username":username}

        r = requests.post('http://127.0.0.1:8000/api/v1/db/read', json=request_obj)

        if r.status_code == 200:

            request_obj = {"table":"WebUser", "operation":"delete","username":username,"op":"delete"}
            
            r = requests.post('http://127.0.0.1:8000/api/v1/db/write', json=request_obj)

            if r.status_code == 200:
                return JsonResponse({"message":"User Deleted Successfully"}, safe=False, status=200)
            elif r.status_code == 400:
                return JsonResponse({"message":"User Delete Failed"}, safe=False, status=400)
            else:
                return JsonResponse({"message":"Unknown Error"}, safe=False, status=501)

        else:
            return JsonResponse({"message":"Username Not Found"}, safe=False, status=400)
            
    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


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
            table = "WebUser"
            cur_model = apps.get_model('userapi',table)

            cur_model.objects.all().delete()

            return JsonResponse({"message":"Cleared Successfully"}, safe=False, status=200)

        except:
            return JsonResponse({"message":"Bad Request"}, safe=False, status=400)
    
    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def readDb(request):

    if request.method == 'POST':

        json_body = json.loads(request.body)
        table = json_body['table']
        cur_model = apps.get_model('userapi', table)

        if table == "WebUser":

            operation = json_body['operation']
            if operation == 'get':

                username = json_body['username']
                try:
                    user = cur_model.objects.all().get(username=username).username
                    response_dict = {"user": user}
                    return JsonResponse(response_dict,safe=False,status=200)

                except:
                    return JsonResponse({"message":"Username not found"}, safe=False, status=400)
            
            elif operation == 'all':

                try:
                    all_users = cur_model.objects.values_list('username',flat=True)
                    users_list = list(all_users)

                    response_dict = {"users_list": users_list}
                    return JsonResponse(response_dict,safe=False,status=200)
                
                except:
                    return JsonResponse({"message":"Unknown Error"}, safe=False, status=400)

            else:
                return JsonResponse({"message":"Invalid Operation"}, safe=False, status=400)
        else :
            return JsonResponse({"message":"Model Not Found"}, safe=False, status=400)
    
    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def writeDb(request):

    if request.method == 'POST':

        json_body = json.loads(request.body)

        table = json_body['table']
        cur_model = apps.get_model('userapi', table)


        if table == "WebUser":

            operation = json_body['operation']

            if(operation == "insert"):

                username = json_body['username']
                password = json_body['password']

                try:
                    user_instance = cur_model(username,password)
                    user_instance.save()
                    return JsonResponse({"message":"Successfully Written to db"}, safe=False, status=200)

                except:
                    return JsonResponse({"message":"Write Failed"}, safe=False, status=400)

            elif( operation == 'delete'):

                username = json_body['username']

                try:
                    user_instance = cur_model.objects.get(username = username)
                    user_instance.delete()
                    return JsonResponse({"message":"User Deleted Successfully"}, safe=False, status=200)

                except:
                    return JsonResponse({"message":"User Delete Failed!"}, safe=False, status=400)
            
            else :
                return JsonResponse({"message":"Invalid Operation"}, safe=False, status=400)

    else:
        return JsonResponse({"message":"Wrong Http Method"}, safe=False, status=405)


def requestMade():
    
    with open("file.txt", "r") as f_read:
        count = int(f_read.readline())

    count = count + 1

    with open("file.txt", "w") as f_write:
        f_write.write(str(count))
